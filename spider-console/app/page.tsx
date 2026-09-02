"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { Ago } from "@/components/ago";
import { StatusBadge } from "@/components/status-badge";
import { duration, isLive, sha, sortedStatusCounts, runDuration, taskDuration } from "@/lib/types";

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
  const [failingCount, setFailingCount] = useState<number | null>(null);
  const [retryNote, setRetryNote] = useState<string | null>(null);

  const scrapeAll = async () => {
    setRetryNote("enqueueing a full sweep…");
    try {
      const response = await fetch("/api/scrape-all", { method: "POST" });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setRetryNote(
          `sweep queued: ${Number(body?.enqueued ?? 0)} entries enqueued, ${Number(body?.skipped ?? 0)} without an activated scraper skipped`,
        );
      } else {
        setRetryNote(String(body?.detail ?? body?.error ?? `HTTP ${response.status}`));
      }
    } catch (exc) {
      setRetryNote(String(exc));
    }
  };

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

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch("/api/runs", { cache: "no-store" });
        const body = (await response.json()) as unknown[] | { error: string };
        if (!cancelled && Array.isArray(body)) setFailingCount(body.length);
      } catch {
        // The scraping panel just shows "…" until the next poll succeeds.
      }
    };
    load();
    const timer = setInterval(load, 10_000);
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
  const budget = usage && !usage.error ? usage.budget : null;
  const live = tasks.filter(isLive);
  // A failed task is only a problem while it is the entry's latest word:
  // an exhausted create superseded by a later successful one is history.
  const latestTaskByEntry = new Map<string, string>();
  for (const task of tasks) {
    const key = task.entry_id ?? task.id;
    if (!latestTaskByEntry.has(key)) latestTaskByEntry.set(key, task.id);
  }
  const problems = tasks
    .filter(
      (task) =>
        task.last_error &&
        task.status !== "succeeded" &&
        !isLive(task) &&
        latestTaskByEntry.get(task.entry_id ?? task.id) === task.id,
    )
    .slice(0, 8);
  const recentRuns = runs.slice(0, 10);

  return (
    <div className="grid">
      <section className="panel wide">
        <h2>
          Scraping{" "}
          <button
            className="action"
            title="Enqueue one run for every entry with an activated scraper (deterministic, no LLM). Repeating within the same hour reuses the existing jobs."
            onClick={scrapeAll}
          >
            scrape all
          </button>{" "}
          <Link className="more" href="/runs">
            triage →
          </Link>
        </h2>
        {retryNote ? <p className="note">{retryNote}</p> : null}
        {stats ? (
          <div className="counts">
            <Link className="count" href="/entries">
              <div className="value">{stats.entries}</div>
              <div className="label">entries</div>
            </Link>
            <div className="count">
              <div className="value">{stats.records}</div>
              <div className="label">records</div>
            </div>
            <Link
              className="count"
              href="/runs"
              title="Entries whose most recent run failed and no run has succeeded since"
            >
              <div className="value">{failingCount ?? "…"}</div>
              <div className="label">still failing</div>
            </Link>
            <Link className="count" href="/runs?filter=succeeded">
              <div className="value">{stats.execution_runs?.["succeeded"] ?? 0}</div>
              <div className="label">runs ok</div>
            </Link>
          </div>
        ) : (
          <p className="error">{executor.error ?? "stats unavailable"}</p>
        )}
      </section>

      <section className="panel wide">
        <h2>
          Recent runs{" "}
          <Link className="more" href="/runs?filter=all">
            all runs →
          </Link>
        </h2>
        <div className="scroll">
          <table>
            <thead>
              <tr>
                <th>run</th>
                <th>entry</th>
                <th>status</th>
                <th>failure</th>
                <th>release</th>
                <th>started</th>
                <th title="Wall-clock time from run start to finish">duration</th>
                <th>actions</th>
              </tr>
            </thead>
            <tbody>
              {recentRuns.map((run) => (
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
                  <td><Ago iso={run.started_at} /></td>
                  <td>{runDuration(run.started_at, run.finished_at)}</td>
                  <td className="actions">
                    <button
                      className="action"
                      title="Run this entry's scraper again now (deterministic, no LLM)"
                      onClick={() => retry(run.entry_id)}
                    >
                      retry
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <div className="panel-row">
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
        <h2>
          Doctor tasks{" "}
          <Link className="more" href="/tasks">
            all →
          </Link>
        </h2>
        {executor.error ? (
          <p className="error">{executor.error}</p>
        ) : stats ? (
          <>
            <div
              className="status-bar"
              title="Share of Doctor tasks by status"
            >
              {sortedStatusCounts(stats.doctor_tasks).map(([status, count]) => (
                <div
                  key={status}
                  className={`seg st-${status}`}
                  style={{ flexGrow: count }}
                  title={`${status.replace(/_/g, " ")}: ${count}`}
                />
              ))}
            </div>
            <div className="counts">
              <div className="count">
                <div className={`value ${live.length ? "st-running" : ""}`}>
                  {live.length}
                </div>
                <div className="label">working now</div>
              </div>
              {sortedStatusCounts(stats.doctor_tasks).map(([status, count]) => (
                <Link
                  className="count"
                  key={status}
                  href={`/tasks?status=${encodeURIComponent(status)}`}
                >
                  <div className={`value st-${status}`}>{count}</div>
                  <div className="label">{status.replace(/_/g, " ")}</div>
                </Link>
              ))}
            </div>
          </>
        ) : null}
      </section>

      {stats?.doctor_throughput ? (
        <section className="panel">
          <h2>Doctor progress</h2>
          {(() => {
            const t = stats.doctor_throughput;
            const line = (succeeded: number, finished: number) => {
              if (!finished) return "no attempts finished";
              const pct = Math.round((100 * succeeded) / finished);
              return (
                <>
                  <b className={succeeded ? "st-succeeded" : "st-failed"}>
                    {succeeded}
                  </b>{" "}
                  scraper{succeeded === 1 ? "" : "s"} built of{" "}
                  <b>{finished}</b> attempt{finished === 1 ? "" : "s"} ({pct}%
                  success)
                </>
              );
            };
            const queued = stats.doctor_tasks["queued"] ?? 0;
            const rate = t.finished_1h;
            const hours = rate ? queued / rate : null;
            const eta =
              hours === null
                ? null
                : hours >= 48
                  ? `~${Math.round(hours / 24)} days`
                  : hours >= 1.5
                    ? `~${Math.round(hours)} hours`
                    : `~${Math.max(1, Math.round(hours * 60))} minutes`;
            return (
              <ul className="progress-lines">
                <li>
                  <span className="label">last hour</span> {line(t.succeeded_1h, t.finished_1h)}
                </li>
                <li>
                  <span className="label">last 24h</span> {line(t.succeeded_24h, t.finished_24h)}
                </li>
                <li>
                  <span className="label">queue</span>{" "}
                  {queued === 0 ? (
                    "empty"
                  ) : (
                    <>
                      <b className="st-queued">{queued}</b> waiting
                      {eta ? ` · drained in ${eta} at the last hour's pace` : " · no attempts finished in the last hour"}
                    </>
                  )}
                </li>
              </ul>
            );
          })()}
        </section>
      ) : null}
      </div>

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
                  <th title="How long the current attempt has been running (since claim)">duration</th>
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
                    <td>{taskDuration(task)}</td>
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
                  <th title="Why this task's most recent attempt failed; retries overwrite it. Each create/repair cycle is its own task row, so an entry can have several">error</th>
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
