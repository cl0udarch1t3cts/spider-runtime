"use client";

import { useEffect, useState } from "react";

interface Lease {
  worker_id: string | null;
  expires_at: string | null;
}

interface DoctorTask {
  id: string;
  entry_id: string | null;
  type: string | null;
  status: string | null;
  attempts: number;
  max_attempts: number;
  failure_class: string | null;
  last_error: string | null;
  candidate_sha: string | null;
  updated_at: string | null;
  lease: Lease | null;
}

interface Run {
  id: string;
  entry_id: string;
  status: string;
  failure_class: string | null;
  record_id: string | null;
  scraper_release: string | null;
  started_at: string;
  finished_at: string | null;
}

interface EntryRow {
  id: string;
  businessname: string | null;
  website: string | null;
  active: boolean;
  scraper_release: string | null;
  updated_at: string | null;
}

interface Overview {
  generatedAt: string;
  executor: {
    error?: string;
    stats?: {
      entries: number;
      records: number;
      doctor_tasks: Record<string, number>;
      execution_jobs: Record<string, number>;
      execution_runs: Record<string, number>;
    };
    tasks?: DoctorTask[];
    runs?: Run[];
    entries?: EntryRow[];
  };
  usage: {
    error?: string;
    source?: string;
    budget?: {
      usedPercent: number;
      allowedPercent: number;
      day: number | null;
      totalDays: number | null;
      resetsInSeconds: number | null;
      dailyPercent: number;
      reservePercent: number;
      decision: string;
    } | null;
  } | null;
}

function ago(iso: string | null): string {
  if (!iso) return "—";
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 90) return `${Math.round(seconds)}s ago`;
  if (seconds < 5400) return `${Math.round(seconds / 60)}m ago`;
  if (seconds < 129_600) return `${Math.round(seconds / 3600)}h ago`;
  return `${Math.round(seconds / 86_400)}d ago`;
}

function duration(seconds: number | null): string {
  if (seconds === null) return "—";
  const days = Math.floor(seconds / 86_400);
  const hours = Math.floor((seconds % 86_400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return days ? `${days}d${hours}h` : `${hours}h${minutes}m`;
}

function sha(value: string | null): string {
  return value ? value.slice(0, 10) : "—";
}

function isLive(task: DoctorTask): boolean {
  return (
    task.status === "running" &&
    !!task.lease?.expires_at &&
    new Date(task.lease.expires_at).getTime() > Date.now()
  );
}

function StatusBadge({ value }: { value: string | null }) {
  return <span className={`status ${value ?? ""}`}>{value ?? "—"}</span>;
}

export default function Dashboard() {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch("/api/overview", { cache: "no-store" });
        if (!response.ok) throw new Error(`overview returned ${response.status}`);
        const payload = (await response.json()) as Overview;
        if (!cancelled) {
          setData(payload);
          setError(null);
        }
      } catch (exc) {
        if (!cancelled) setError(String(exc));
      }
    };
    load();
    const timer = setInterval(load, 5000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  if (!data) {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  const { executor, usage } = data;
  const stats = executor.stats;
  const tasks = executor.tasks ?? [];
  const runs = executor.runs ?? [];
  const entries = executor.entries ?? [];
  const budget = usage && !usage.error ? usage.budget : null;
  const live = tasks.filter(isLive);

  return (
    <main>
      <div className="header">
        <div className="brand">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.svg" alt="Cloud Architects" width={30} height={30} />
          <div>
            <h1>SPIDER CONSOLE</h1>
            <span className="tagline">
              Cloud Architects GmbH · Cloud-Native Software &amp; Architecture
              Experts
            </span>
          </div>
        </div>
        <span className="meta">
          refreshed {ago(data.generatedAt)}
          {error ? <span className="error"> — {error}</span> : null}
        </span>
      </div>

      <div className="grid">
        <section className="panel">
          <h2>Subscription budget</h2>
          {budget ? (
            <>
              <div className="bar">
                <div
                  className={`fill ${
                    budget.usedPercent >= budget.allowedPercent
                      ? "over"
                      : budget.usedPercent >= budget.allowedPercent - 10
                        ? "warn"
                        : ""
                  }`}
                  style={{ width: `${Math.min(100, budget.usedPercent)}%` }}
                />
                <div
                  className="limit"
                  style={{ left: `${Math.min(100, budget.allowedPercent)}%` }}
                />
                <div className="text">
                  {budget.usedPercent.toFixed(1)}% used /{" "}
                  {budget.allowedPercent.toFixed(0)}% allowed
                </div>
              </div>
              <p className="muted">
                decision: <StatusBadge value={budget.decision === "proceed" ? "succeeded" : "failed"} />{" "}
                {budget.decision}
                {budget.day !== null
                  ? ` · day ${budget.day}/${budget.totalDays}`
                  : ""}{" "}
                · resets in {duration(budget.resetsInSeconds)} · daily{" "}
                {budget.dailyPercent}% · reserve {budget.reservePercent}%
              </p>
            </>
          ) : (
            <p className="error">
              usage unavailable{usage?.error ? ` — ${usage.error}` : ""}
            </p>
          )}
        </section>

        <section className="panel">
          <h2>Totals</h2>
          {executor.error ? (
            <p className="error">{executor.error}</p>
          ) : stats ? (
            <div className="counts">
              <div className="count">
                <div className="value">{live.length}</div>
                <div className="label">live tasks</div>
              </div>
              <div className="count">
                <div className="value">{stats.entries}</div>
                <div className="label">entries</div>
              </div>
              <div className="count">
                <div className="value">{stats.records}</div>
                <div className="label">records</div>
              </div>
              {Object.entries(stats.doctor_tasks).map(([status, count]) => (
                <div className="count" key={status}>
                  <div className="value">{count}</div>
                  <div className="label">tasks {status}</div>
                </div>
              ))}
            </div>
          ) : null}
        </section>

        <section className="panel wide">
          <h2>Doctor tasks</h2>
          <table>
            <thead>
              <tr>
                <th>entry</th>
                <th>type</th>
                <th>status</th>
                <th>att</th>
                <th>worker / lease</th>
                <th>candidate</th>
                <th>updated</th>
                <th>last error</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr key={task.id}>
                  <td title={task.id}>{task.entry_id ?? "—"}</td>
                  <td>{task.type}</td>
                  <td>
                    <StatusBadge value={task.status} />
                    {isLive(task) ? " ●" : ""}
                  </td>
                  <td>
                    {task.attempts}/{task.max_attempts}
                  </td>
                  <td>
                    {task.lease
                      ? `${task.lease.worker_id} → ${ago(task.lease.expires_at)}`
                      : "—"}
                  </td>
                  <td>{sha(task.candidate_sha)}</td>
                  <td>{ago(task.updated_at)}</td>
                  <td className="err-cell" title={task.last_error ?? ""}>
                    {task.last_error ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel wide">
          <h2>Execution runs</h2>
          <table>
            <thead>
              <tr>
                <th>run</th>
                <th>entry</th>
                <th>status</th>
                <th>failure</th>
                <th>release</th>
                <th>record</th>
                <th>started</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => (
                <tr key={run.id}>
                  <td>{run.id.slice(0, 12)}</td>
                  <td>{run.entry_id}</td>
                  <td>
                    <StatusBadge value={run.status} />
                  </td>
                  <td>{run.failure_class ?? "—"}</td>
                  <td>{sha(run.scraper_release)}</td>
                  <td>{run.record_id ? run.record_id.slice(0, 12) : "—"}</td>
                  <td>{ago(run.started_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel wide">
          <h2>Entries</h2>
          <table>
            <thead>
              <tr>
                <th>entry</th>
                <th>business</th>
                <th>website</th>
                <th>active</th>
                <th>release</th>
                <th>updated</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.id}</td>
                  <td>{entry.businessname ?? "—"}</td>
                  <td>{entry.website ?? "—"}</td>
                  <td>{entry.active ? "yes" : "no"}</td>
                  <td>{sha(entry.scraper_release)}</td>
                  <td>{ago(entry.updated_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </main>
  );
}
