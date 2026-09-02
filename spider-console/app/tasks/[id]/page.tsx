"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

interface TranscriptMessage {
  role: string;
  tool_name: string | null;
  content: string;
  content_chars: number;
  timestamp: number | null;
}

interface Transcript {
  task_id: string;
  session: Record<string, unknown> | null;
  messages: TranscriptMessage[];
}

function messageTime(timestamp: number | null): string {
  if (!timestamp) return "";
  // Hermes stores epoch seconds (floats).
  return new Date(timestamp * 1000).toLocaleTimeString();
}

function tokens(session: Record<string, unknown>, key: string): string {
  const value = session[key];
  return typeof value === "number" ? value.toLocaleString("en-US") : "—";
}

export default function TranscriptPage() {
  const params = useParams<{ id: string }>();
  const taskId = decodeURIComponent(params.id);
  const [data, setData] = useState<Transcript | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [full, setFull] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch(
          `/api/transcript/${encodeURIComponent(taskId)}${full ? "?full=1" : ""}`,
          { cache: "no-store" },
        );
        const body = (await response.json()) as Transcript | { error: string };
        if (cancelled) return;
        if ("error" in body) {
          setError(body.error);
        } else {
          setData(body);
          setError(null);
        }
      } catch (exc) {
        if (!cancelled) setError(String(exc));
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, [taskId, full]);

  const session = data?.session ?? null;
  const truncated = (data?.messages ?? []).some(
    (message) => message.content.length < message.content_chars,
  );

  return (
    <div className="grid">
      <section className="panel wide">
        <h2>
          Doctor transcript <span className="muted">{taskId}</span>
        </h2>
        <p className="muted">
          <Link className="link" href="/tasks">
            ← all tasks
          </Link>
        </p>
        {error ? <p className="error">{error}</p> : null}
        {!data && !error ? <p className="muted">loading…</p> : null}
        {session ? (
          <p className="muted">
            model {String(session.model ?? "—")} · {tokens(session, "api_call_count")} LLM
            calls · input {tokens(session, "input_tokens")} · output{" "}
            {tokens(session, "output_tokens")} · cache read{" "}
            {tokens(session, "cache_read_tokens")} · reasoning{" "}
            {tokens(session, "reasoning_tokens")}
          </p>
        ) : null}
        {truncated && !full ? (
          <p>
            <button className="chip" onClick={() => setFull(true)}>
              long messages are truncated — load full transcript
            </button>
          </p>
        ) : null}
        {(data?.messages ?? []).map((message, index) => (
          <div className="transcript-message" key={index}>
            <div className="transcript-meta">
              <span className={`transcript-role role-${message.role}`}>
                {message.role}
                {message.tool_name ? ` · ${message.tool_name}` : ""}
              </span>
              <span className="muted">{messageTime(message.timestamp)}</span>
            </div>
            {message.content ? (
              <pre className="transcript-body">
                {message.content}
                {message.content.length < message.content_chars
                  ? `\n…[truncated, ${message.content_chars.toLocaleString("en-US")} chars total]`
                  : ""}
              </pre>
            ) : null}
          </div>
        ))}
      </section>
    </div>
  );
}
