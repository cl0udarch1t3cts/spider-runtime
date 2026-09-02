"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { StatusBadge } from "@/components/status-badge";

interface RunLog {
  id: string;
  entry_id: string | null;
  status: string | null;
  log_tail: string | null;
}

export default function RunLogPage() {
  const params = useParams<{ id: string }>();
  const runId = decodeURIComponent(params.id);
  const [data, setData] = useState<RunLog | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);

  const retry = async (entryId: string) => {
    setNote("enqueueing…");
    try {
      const response = await fetch("/api/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entryId }),
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setNote(
          `job ${String(body?.id ?? "").slice(0, 12)} queued — the fresh run gets its own log page`,
        );
      } else {
        setNote(String(body?.detail ?? body?.error ?? `HTTP ${response.status}`));
      }
    } catch (exc) {
      setNote(String(exc));
    }
  };

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch(`/api/run-log/${encodeURIComponent(runId)}`, {
          cache: "no-store",
        });
        const body = (await response.json()) as RunLog | { error: string };
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
  }, [runId]);

  return (
    <div className="grid">
      <section className="panel wide">
        <h2>
          Run log <span className="muted">{runId}</span>
        </h2>
        <p className="muted">
          <Link className="link" href="/runs">
            ← all runs
          </Link>
          {data?.entry_id ? (
            <>
              {" · "}
              <Link
                className="link"
                href={`/entries/${encodeURIComponent(data.entry_id)}`}
              >
                {data.entry_id}
              </Link>
            </>
          ) : null}
          {data?.status ? (
            <>
              {" · "}
              <StatusBadge value={data.status} />
            </>
          ) : null}
          {data?.entry_id ? (
            <>
              {" · "}
              <button
                className="action"
                title="Run this entry's scraper again now (deterministic, no LLM)"
                onClick={() => retry(data.entry_id!)}
              >
                retry
              </button>
            </>
          ) : null}
        </p>
        {note ? <p className="note">{note}</p> : null}
        {error ? <p className="error">{error}</p> : null}
        {!data && !error ? <p className="muted">loading…</p> : null}
        {data ? (
          data.log_tail ? (
            <pre className="transcript-body log-tail">{data.log_tail}</pre>
          ) : (
            <p className="muted">
              this run recorded no log output (runs before the log-capture
              deploy, or a scraper that wrote nothing to stderr)
            </p>
          )
        ) : null}
      </section>
    </div>
  );
}
