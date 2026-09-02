"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { StatusBadge } from "@/components/status-badge";

interface RunLog {
  id: string;
  entry_id: string | null;
  status: string | null;
  failure_class: string | null;
  errors: string[];
  log_tail: string | null;
}

export default function RunLogPage() {
  const params = useParams<{ id: string }>();
  const runId = decodeURIComponent(params.id);
  const router = useRouter();
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
      if (response.ok && body?.id) {
        // A fresh console job runs as attempt 1, so its run id is knowable
        // before the worker even starts it; the log page waits for it.
        router.push(`/runs/${encodeURIComponent(`${String(body.id)}:1`)}`);
      } else {
        setNote(String(body?.detail ?? body?.error ?? `HTTP ${response.status}`));
      }
    } catch (exc) {
      setNote(String(exc));
    }
  };

  useEffect(() => {
    let cancelled = false;
    setData(null);
    setError(null);
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
    // Keep polling: a just-enqueued run materializes once the worker picks
    // it up, and a running one grows its log until it finishes.
    const timer = setInterval(load, 5000);
    return () => {
      cancelled = true;
      clearInterval(timer);
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
        {error ? (
          /returned 404/.test(error) ? (
            <p className="muted">waiting for the worker to start this run…</p>
          ) : (
            <p className="error">{error}</p>
          )
        ) : null}
        {!data && !error ? <p className="muted">loading…</p> : null}
        {data?.failure_class || data?.errors?.length ? (
          <>
            <h3 className="log-section">
              failure{data.failure_class ? `: ${data.failure_class}` : ""}
            </h3>
            <pre className="transcript-body log-tail errors">
              {data.errors.length ? data.errors.join("\n\n") : "no error details recorded"}
            </pre>
          </>
        ) : null}
        {data ? (
          data.log_tail ? (
            <>
              <h3 className="log-section">scraper log</h3>
              <pre className="transcript-body log-tail">{data.log_tail}</pre>
            </>
          ) : (
            <p className="muted">
              {data.failure_class || data.errors?.length
                ? "the scraper itself wrote no log output — the failure above was recorded by the executor (validation, classification), not by the script"
                : "this run recorded no log output (runs before the log-capture deploy, or a scraper that wrote nothing to stderr)"}
            </p>
          )
        ) : null}
      </section>
    </div>
  );
}
