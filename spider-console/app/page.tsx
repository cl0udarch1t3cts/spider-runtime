"use client";

import Link from "next/link";
import { useOverview } from "@/components/overview-provider";
import { StatusBadge } from "@/components/status-badge";
import { ago, duration, isLive, sha } from "@/lib/types";

export default function OverviewPage() {
  const { data, error } = useOverview();

  if (!data) {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  const { executor, usage } = data;
  const stats = executor.stats;
  const tasks = executor.tasks ?? [];
  const runs = executor.runs ?? [];
  const budget = usage && !usage.error ? usage.budget : null;
  const live = tasks.filter(isLive);
  const problems = tasks
    .filter(
      (task) =>
        task.last_error &&
        task.status !== "succeeded" &&
        !isLive(task),
    )
    .slice(0, 8);
  const recentRuns = runs.slice(0, 10);

  return (
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
              decision:{" "}
              <StatusBadge
                value={budget.decision === "proceed" ? "succeeded" : "failed"}
              />{" "}
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
            <Link className="count" href="/entries">
              <div className="value">{stats.entries}</div>
              <div className="label">entries</div>
            </Link>
            <div className="count">
              <div className="value">{stats.records}</div>
              <div className="label">records</div>
            </div>
            {Object.entries(stats.doctor_tasks).map(([status, count]) => (
              <Link
                className="count"
                key={status}
                href={`/tasks?status=${encodeURIComponent(status)}`}
              >
                <div className="value">{count}</div>
                <div className="label">tasks {status}</div>
              </Link>
            ))}
          </div>
        ) : null}
      </section>

      <section className="panel wide">
        <h2>
          Live now{" "}
          <Link className="more" href="/tasks">
            all tasks →
          </Link>
        </h2>
        {live.length ? (
          <div className="scroll">
            <table>
              <thead>
                <tr>
                  <th>entry</th>
                  <th>type</th>
                  <th>att</th>
                  <th>worker / lease</th>
                  <th>updated</th>
                </tr>
              </thead>
              <tbody>
                {live.map((task) => (
                  <tr key={task.id}>
                    <td title={task.id}>
                      {task.entry_id ? (
                        <Link
                          className="link"
                          href={`/entries/${encodeURIComponent(task.entry_id)}`}
                        >
                          {task.entry_id}
                        </Link>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td>{task.type}</td>
                    <td>
                      {task.attempts}/{task.max_attempts}
                    </td>
                    <td>
                      {task.lease
                        ? `${task.lease.worker_id} → ${ago(task.lease.expires_at)}`
                        : "—"}
                    </td>
                    <td>{ago(task.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="muted">no Doctor task is running right now</p>
        )}
      </section>

      <section className="panel wide">
        <h2>
          Recent runs{" "}
          <Link className="more" href="/runs">
            all runs →
          </Link>
        </h2>
        <div className="scroll">
          <table>
            <thead>
              <tr>
                <th>entry</th>
                <th>status</th>
                <th>failure</th>
                <th>release</th>
                <th>started</th>
              </tr>
            </thead>
            <tbody>
              {recentRuns.map((run) => (
                <tr key={run.id}>
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

      {problems.length ? (
        <section className="panel wide">
          <h2>Needs attention</h2>
          <div className="scroll">
            <table>
              <thead>
                <tr>
                  <th>entry</th>
                  <th>status</th>
                  <th>att</th>
                  <th>last error</th>
                  <th>updated</th>
                </tr>
              </thead>
              <tbody>
                {problems.map((task) => (
                  <tr key={task.id}>
                    <td title={task.id}>
                      {task.entry_id ? (
                        <Link
                          className="link"
                          href={`/entries/${encodeURIComponent(task.entry_id)}`}
                        >
                          {task.entry_id}
                        </Link>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td>
                      <StatusBadge value={task.status} />
                    </td>
                    <td>
                      {task.attempts}/{task.max_attempts}
                    </td>
                    <td className="err-cell" title={task.last_error ?? ""}>
                      {task.last_error}
                    </td>
                    <td>{ago(task.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ) : null}
    </div>
  );
}
