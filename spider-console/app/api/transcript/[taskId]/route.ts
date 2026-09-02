import { NextResponse } from "next/server";
import { copyFile, mkdtemp, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";

export const dynamic = "force-dynamic";

// Read-only mount of the Doctor's data/tasks directory (credential-free
// per-task Hermes homes; the broker's OAuth volume is never mounted here).
const TASKS_DIR = process.env.DOCTOR_TASKS_DIR ?? "";
const TASK_ID = /^[A-Za-z0-9_.-]{1,64}$/;
const SNIPPET = 4_000;

export interface TranscriptMessage {
  role: string;
  tool_name: string | null;
  content: string;
  content_chars: number;
  timestamp: number | null;
}

export async function GET(
  request: Request,
  { params }: { params: Promise<{ taskId: string }> },
) {
  const { taskId } = await params;
  if (!TASK_ID.test(taskId) || taskId.startsWith(".")) {
    return NextResponse.json({ error: "invalid task id" }, { status: 400 });
  }
  if (!TASKS_DIR) {
    return NextResponse.json(
      { error: "DOCTOR_TASKS_DIR is not configured" },
      { status: 503 },
    );
  }
  const full = new URL(request.url).searchParams.get("full") === "1";
  const home = path.join(TASKS_DIR, taskId, "hermes-home");
  if (!existsSync(path.join(home, "state.db"))) {
    return NextResponse.json(
      { error: "no transcript for this task (no persisted Hermes home)" },
      { status: 404 },
    );
  }

  // The mount is read-only and the WAL sidecars may still exist, so SQLite
  // cannot recover in place; work on a throwaway copy instead.
  const scratch = await mkdtemp(path.join(tmpdir(), "transcript-"));
  try {
    for (const suffix of ["", "-wal", "-shm"]) {
      const source = path.join(home, `state.db${suffix}`);
      if (existsSync(source)) {
        await copyFile(source, path.join(scratch, `state.db${suffix}`));
      }
    }
    const db = new DatabaseSync(path.join(scratch, "state.db"), {
      readOnly: false,
    });
    try {
      const session = db
        .prepare(
          `SELECT model, message_count, api_call_count, input_tokens,
                  output_tokens, cache_read_tokens, reasoning_tokens,
                  started_at, ended_at, end_reason
             FROM sessions LIMIT 1`,
        )
        .get() as Record<string, unknown> | undefined;
      const messages = (
        db
          .prepare(
            `SELECT role, tool_name, coalesce(content, '') AS content, timestamp
               FROM messages ORDER BY id`,
          )
          .all() as {
          role: string;
          tool_name: string | null;
          content: string;
          timestamp: number | null;
        }[]
      ).map((message) => ({
        role: message.role,
        tool_name: message.tool_name,
        content: full ? message.content : message.content.slice(0, SNIPPET),
        content_chars: message.content.length,
        timestamp: message.timestamp,
      }));
      return NextResponse.json({ task_id: taskId, session: session ?? null, messages });
    } finally {
      db.close();
    }
  } catch (exc) {
    return NextResponse.json({ error: String(exc) }, { status: 500 });
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
}
