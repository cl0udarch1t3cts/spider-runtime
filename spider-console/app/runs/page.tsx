"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { StatusBadge } from "@/components/status-badge";
import { ago, sha } from "@/lib/types";

type Filter = "all" | "succeeded" | "failed";

export default function RunsPage() {
  const { data, error } = useOverview();
  const [filter, setFilter] = useState<Filter>("all");

  const runs = useMemo(() => data?.executor.runs ?? [], [data]);
  const filtered = useMemo(() => {
    if (filter === "all") return runs;
    if (filter === "succeeded")
      return runs.filter((run) => run.status === "succeeded");
    return runs.filter((run) => run.status !== "succeeded");
  }, [runs, filter]);

  if (!data) {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  return (
    <div className="grid">
      <section className="panel wide">
        <div className="toolbar">
          <div className="chips">
            {(["all", "succeeded", "failed"] as Filter[]).map((name) => (
              <button
                key={name}
                className={`chip ${filter === name ? "active" : ""}`}
                onClick={() => setFilter(name)}
              >
                {name}
              </button>
            ))}
          </div>
          <span className="muted">latest {runs.length} runs shown</span>
        </div>
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
              {filtered.map((run) => (
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
