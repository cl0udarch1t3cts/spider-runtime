"use client";

import Link from "next/link";
import { useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { Ago } from "@/components/ago";
import { StatusBadge } from "@/components/status-badge";
import { duration, isLive, sha, sortedStatusCounts, runDuration } from "@/lib/types";

function BudgetEditor({
  dailyPercent,
  reservePercent,
}: {
  dailyPercent: number;
  reservePercent: number;
}) {
  const [editing, setEditing] = useState(false);
  const [daily, setDaily] = useState(String(dailyPercent));
  const [reserve, setReserve] = useState(String(reservePercent));
  const [note, setNote] = useState<string | null>(null);

  const apply = async () => {
    setNote("saving…");
    try {
      const response = await fetch("/api/doctor-control", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          daily_percent: Number(daily),
          reserve_percent: Number(reserve),
        }),
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setNote("saved — the Doctor applies it within ~5 minutes");
        setEditing(false);
      } else {
        setNote(String(body?.detail?.[0]?.msg ?? body?.error ?? `HTTP ${response.status}`));
      }
    } catch (exc) {
      setNote(String(exc));
    }
  };

  if (!editing) {
    return (
      <span>
        <button
          className="link"
          title="Change the Doctor's daily job budget and development reserve"
          onClick={() => {
            setDaily(String(dailyPercent));
            setReserve(String(reservePercent));
            setNote(null);
            setEditing(true);
          }}
        >
          (adjust)
        </button>
        {note ? <span className="note"> {note}</span> : null}
      </span>
    );
  }
  return (
    <span className="budget-editor">
      daily{" "}
      <input
        className="search pct"
        type="number"
        min={1}
        max={100}
        value={daily}
        onChange={(event) => setDaily(event.target.value)}
      />
      % · reserve{" "}
      <input
        className="search pct"
        type="number"
        min={0}
        max={99}
        value={reserve}
        onChange={(event) => setReserve(event.target.value)}
      />
      %{" "}
      <button className="action" onClick={apply}>
        apply
      </button>{" "}
      <button className="action secondary" onClick={() => setEditing(false)}>
        cancel
      </button>
      {note ? <span className="note"> {note}</span> : null}
    </span>
  );
}

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
              {budget.dailyPercent}% · reserve {budget.reservePercent}%{" "}
              <BudgetEditor
                dailyPercent={budget.dailyPercent}
                reservePercent={budget.reservePercent}
              />
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
            {sortedStatusCounts(stats.doctor_tasks).map(([status, count]) => (
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

      {stats?.doctor_throughput ? (
        <section className="panel">
          <h2>Doctor progress</h2>
          <div className="counts">
            <div className="count">
              <div className="value">{stats.doctor_throughput.succeeded_1h}</div>
              <div className="label">succeeded / 1h</div>
            </div>
            <div className="count">
              <div className="value">{stats.doctor_throughput.succeeded_24h}</div>
              <div className="label">succeeded / 24h</div>
            </div>
            <div className="count">
              <div className="value">{stats.doctor_throughput.finished_1h}</div>
              <div className="label">finished / 1h</div>
            </div>
            <div className="count">
              <div className="value">{stats.doctor_throughput.finished_24h}</div>
              <div className="label">finished / 24h</div>
            </div>
          </div>
          <p className="muted">
            {(() => {
              const queued = stats.doctor_tasks["queued"] ?? 0;
              const rate = stats.doctor_throughput.finished_1h;
              if (!queued) return "queue is empty";
              if (!rate) return `${queued} queued · no tasks finished in the last hour`;
              const hours = queued / rate;
              const eta =
                hours >= 48
                  ? `~${Math.round(hours / 24)}d`
                  : hours >= 1.5
                    ? `~${Math.round(hours)}h`
                    : `~${Math.max(1, Math.round(hours * 60))}m`;
              return `${queued} queued · ${eta} to drain at the last hour's pace`;
            })()}
          </p>
        </section>
      ) : null}

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
                  <th title="Time since the Doctor last touched this task: claimed it, finished an attempt, or changed its status">last activity</th>
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
                      {task.lease ? (
                        <>
                          {task.lease.worker_id} → <Ago iso={task.lease.expires_at} />
                        </>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td><Ago iso={task.updated_at} /></td>
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
                <th title="Wall-clock time from run start to finish">duration</th>
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
                  <td><Ago iso={run.started_at} /></td>
                <td>{runDuration(run.started_at, run.finished_at)}</td>
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
                  <th title="Why the Doctor's most recent attempt failed (task-level). Script execution failures show as a run's failure class instead">last error</th>
                  <th title="Time since the Doctor last touched this task: claimed it, finished an attempt, or changed its status">last activity</th>
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
                    <td><Ago iso={task.updated_at} /></td>
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
