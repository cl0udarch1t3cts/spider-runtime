"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { Ago } from "@/components/ago";
import { StatusBadge } from "@/components/status-badge";
import { sha, type Run, runDuration } from "@/lib/types";
import { replaceParam } from "@/lib/url-state";

type Filter = "all" | "succeeded" | "failing";

const FILTERS: { key: Filter; label: string; hint: string }[] = [
  {
    key: "failing",
    label: "still failing",
    hint: "Entries whose most recent run failed and no run has succeeded since. Failures a later run already fixed are not shown",
  },
  { key: "all", label: "all", hint: "Latest runs, newest first" },
  { key: "succeeded", label: "succeeded", hint: "Latest successful runs" },
];

function RunsView() {
  const { data, error } = useOverview();
  const filterParam = useSearchParams().get("filter") as Filter | null;
  // Triage-first: the default view is what needs attention right now.
  const filter: Filter = FILTERS.some((f) => f.key === filterParam)
    ? (filterParam as Filter)
    : "failing";
  const setFilter = (value: Filter) =>
    replaceParam("filter", value === "failing" ? null : value);
  const [failing, setFailing] = useState<Run[] | null>(null);
  const [failingError, setFailingError] = useState<string | null>(null);
  const [retryNote, setRetryNote] = useState<string | null>(null);

  const retry = async (entryId: string) => {
    setRetryNote(`enqueueing ${entryId}…`);
    try {
      const response = await fetch("/api/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entryId }),
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setRetryNote(
          `job ${String(body?.id ?? "").slice(0, 12)} queued for ${entryId} — a fresh run appears once the worker picks it up`,
        );
      } else {
        setRetryNote(
          `${entryId}: ${String(body?.detail ?? body?.error ?? `HTTP ${response.status}`)}`,
        );
      }
    } catch (exc) {
      setRetryNote(`${entryId}: ${String(exc)}`);
    }
  };

  const sendToDoctor = async (runId: string, entryId: string) => {
    setRetryNote(`sending ${entryId} to the Doctor…`);
    try {
      const response = await fetch(`/api/run-repair/${encodeURIComponent(runId)}`, {
        method: "POST",
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setRetryNote(
          `${entryId}: repair task ${String(body?.task_id ?? "").slice(0, 12)} is ${String(body?.status ?? "queued")}`,
        );
      } else {
        setRetryNote(
          `${entryId}: ${String(body?.detail ?? body?.error ?? `HTTP ${response.status}`)}`,
        );
      }
    } catch (exc) {
      setRetryNote(`${entryId}: ${String(exc)}`);
    }
  };

  // "still failing" is a per-entry latest-run view the server computes;
  // the other filters slice the recent-runs window from the overview.
  useEffect(() => {
    if (filter !== "failing") return;
    let cancelled = false;
    setFailing(null);
    const load = async () => {
      try {
        const response = await fetch("/api/runs", { cache: "no-store" });
        const body = (await response.json()) as Run[] | { error: string };
        if (cancelled) return;
        if (Array.isArray(body)) {
          setFailing(body);
          setFailingError(null);
        } else {
          setFailingError(body.error);
        }
      } catch (exc) {
        if (!cancelled) setFailingError(String(exc));
      }
    };
    load();
    const timer = setInterval(load, 10_000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [filter]);

  const recent = useMemo(() => data?.executor.runs ?? [], [data]);
  const rows = useMemo(() => {
    if (filter === "failing") return failing ?? [];
    if (filter === "succeeded")
      return recent.filter((run) => run.status === "succeeded");
    return recent;
  }, [filter, failing, recent]);

  if (!data && filter !== "failing") {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  return (
    <div className="grid">
      <section className="panel wide">
        <div className="toolbar">
          <div className="chips">
            {FILTERS.map((item) => (
              <button
                key={item.key}
                title={item.hint}
                className={`chip ${filter === item.key ? "active" : ""}`}
                onClick={() => setFilter(item.key)}
              >
                {item.label}
              </button>
            ))}
          </div>
          <span className="muted">
            {filter === "failing"
              ? failing
                ? `${failing.length} entries still failing`
                : "loading…"
              : `latest ${rows.length} shown`}
          </span>
        </div>
        {failingError && filter === "failing" ? (
          <p className="error">{failingError}</p>
        ) : null}
        {retryNote ? <p className="note">{retryNote}</p> : null}
        <div className="scroll tall">
          <table>
            <thead>
              <tr>
                <th>run</th>
                <th>entry</th>
                <th>status</th>
                <th>failure</th>
                <th>release</th>
                <th title="Consecutive failed runs since the entry's last success">tries</th>
                <th>started</th>
                <th title="Wall-clock time from run start to finish">duration</th>
                <th>actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((run) => (
                <tr key={run.id}>
                  <td>
                    <Link
                      className="link"
                      title="Open this run's scraper log"
                      href={`/runs/${encodeURIComponent(run.id)}`}
                    >
                      {run.id.slice(0, 12)}
                    </Link>
                  </td>
                  <td>
                    <Link
                      className="link"
                      href={`/entries/${encodeURIComponent(run.entry_id)}`}
                    >
                      {run.entry_id}
                    </Link>
                  </td>
                  <td>
                    <StatusBadge value={run.status} />
                  </td>
                  <td>{run.failure_class ?? "—"}</td>
                  <td>{sha(run.scraper_release)}</td>
                  <td>{run.failed_attempts ?? "—"}</td>
                  <td><Ago iso={run.started_at} /></td>
                <td>{runDuration(run.started_at, run.finished_at)}</td>
                  <td className="actions">
                    <button
                      className="action"
                      title="Run this entry's scraper again now (deterministic, no LLM)"
                      onClick={() => retry(run.entry_id)}
                    >
                      retry
                    </button>{" "}
                    <button
                      className="action"
                      title="Send this broken scrape to the Doctor: queue a repair task (uses LLM budget when claimed)"
                      onClick={() => sendToDoctor(run.id, run.entry_id)}
                    >
                      doctor
                    </button>{" "}
                    <Link
                      className="action"
                      title="Show this entry's Doctor tasks"
                      href={`/tasks?entry=${encodeURIComponent(run.entry_id)}`}
                    >
                      tasks
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default function RunsPage() {
  return (
    <Suspense fallback={<p className="muted">loading…</p>}>
      <RunsView />
    </Suspense>
  );
}
