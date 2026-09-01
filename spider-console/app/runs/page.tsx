"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { StatusBadge } from "@/components/status-badge";
import { ago, sha, type Run } from "@/lib/types";
import { replaceParam } from "@/lib/url-state";

type Filter = "all" | "succeeded" | "failing";

const FILTERS: { key: Filter; label: string; hint: string }[] = [
  { key: "all", label: "all", hint: "Latest runs, newest first" },
  { key: "succeeded", label: "succeeded", hint: "Latest successful runs" },
  {
    key: "failing",
    label: "still failing",
    hint: "Entries whose most recent run failed and no run has succeeded since. Failures a later run already fixed are not shown",
  },
];

function RunsView() {
  const { data, error } = useOverview();
  const filterParam = useSearchParams().get("filter") as Filter | null;
  const filter: Filter = FILTERS.some((f) => f.key === filterParam)
    ? (filterParam as Filter)
    : "all";
  const setFilter = (value: Filter) =>
    replaceParam("filter", value === "all" ? null : value);
  const [failing, setFailing] = useState<Run[] | null>(null);
  const [failingError, setFailingError] = useState<string | null>(null);

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
        <div className="scroll tall">
          <table>
            <thead>
              <tr>
                <th>run</th>
                <th>entry</th>
                <th>status</th>
                <th>failure</th>
                <th>release</th>
                <th>started</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((run) => (
                <tr key={run.id}>
                  <td>{run.id.slice(0, 12)}</td>
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
                  <td>{ago(run.started_at)}</td>
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
