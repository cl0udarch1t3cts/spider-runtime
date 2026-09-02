"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { Ago } from "@/components/ago";
import { StatusBadge } from "@/components/status-badge";
import {
  formatSeconds,
  isLive,
  sha,
  sortedStatusCounts,
  taskDuration,
  type DoctorTask,
} from "@/lib/types";
import { replaceParam } from "@/lib/url-state";

function TasksView() {
  const { data, error } = useOverview();
  const search = useSearchParams();
  const status = search.get("status");
  const entry = search.get("entry");
  const setStatus = (value: string | null) => replaceParam("status", value);
  const [tasks, setTasks] = useState<DoctorTask[] | null>(null);
  const [tasksError, setTasksError] = useState<string | null>(null);

  const counts = data?.executor.stats?.doctor_tasks ?? {};

  // Server-side filtering: with hundreds of task docs, the newest-200 window
  // for the selected status comes from the API, not from slicing the overview.
  useEffect(() => {
    let cancelled = false;
    setTasks(null);
    const load = async () => {
      try {
        const params = new URLSearchParams();
        if (status) params.set("status", status);
        if (entry) params.set("entry", entry);
        const query = params.size ? `?${params}` : "";
        const response = await fetch(`/api/tasks${query}`, {
          cache: "no-store",
        });
        const body = (await response.json()) as
          | DoctorTask[]
          | { error: string };
        if (cancelled) return;
        if (Array.isArray(body)) {
          setTasks(body);
          setTasksError(null);
        } else {
          setTasksError(body.error);
        }
      } catch (exc) {
        if (!cancelled) setTasksError(String(exc));
      }
    };
    load();
    const timer = setInterval(load, 10_000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [status, entry]);

  if (!data && !tasks) {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  return (
    <div className="grid">
      <section className="panel wide">
        <div className="toolbar">
          <div className="chips">
            <button
              className={`chip ${status === null ? "active" : ""}`}
              onClick={() => setStatus(null)}
            >
              all
            </button>
            {sortedStatusCounts(counts).map(([name, count]) => (
              <button
                key={name}
                className={`chip ${status === name ? "active" : ""}`}
                onClick={() => setStatus(status === name ? null : name)}
              >
                {name} <span className="chip-count">{count}</span>
              </button>
            ))}
            {entry ? (
              <button
                className="chip active"
                title="Showing only this entry's tasks; click to clear"
                onClick={() => replaceParam("entry", null)}
              >
                entry: {entry} ✕
              </button>
            ) : null}
          </div>
          <span className="muted">
            {tasks
              ? `newest ${tasks.length}${status ? ` ${status}` : ""} shown`
              : "loading…"}
          </span>
        </div>
        {tasksError ? <p className="error">{tasksError}</p> : null}
        <div className="scroll tall">
          <table>
            <thead>
              <tr>
                <th>entry</th>
                <th>type</th>
                <th>status</th>
                <th>att</th>
                <th>worker / lease</th>
                <th title="How long the current attempt has been running, or how long the recorded attempt took (claim to verified candidate)">duration</th>
                <th>candidate</th>
                <th title="Time since the Doctor last touched this task: claimed it, finished an attempt, or changed its status">last activity</th>
                <th title="Why the Doctor's most recent attempt failed (task-level). Script execution failures show as a run's failure class instead">last error</th>
              </tr>
            </thead>
            <tbody>
              {(tasks ?? []).map((task) => (
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
                    <Link
                      className="link"
                      title="Open the Hermes transcript for this task"
                      href={`/tasks/${encodeURIComponent(task.id)}`}
                    >
                      {task.type}
                    </Link>
                  </td>
                  <td>
                    <StatusBadge value={task.status} />
                    {isLive(task) ? " ●" : ""}
                  </td>
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
                  <td
                    title={
                      task.hermes_seconds !== null && task.hermes_seconds !== undefined
                        ? `Hermes container: ${formatSeconds(task.hermes_seconds)}`
                        : undefined
                    }
                  >
                    {taskDuration(task)}
                  </td>
                  <td>{sha(task.candidate_sha)}</td>
                  <td><Ago iso={task.updated_at} /></td>
                  <td
                    className={`err-cell ${task.status === "succeeded" ? "muted" : ""}`}
                    title={
                      task.last_error
                        ? task.status === "succeeded"
                          ? `From an earlier failed attempt; the task later succeeded. ${task.last_error}`
                          : task.last_error
                        : ""
                    }
                  >
                    {task.last_error
                      ? task.status === "succeeded"
                        ? `earlier attempt: ${task.last_error}`
                        : task.last_error
                      : "—"}
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

export default function TasksPage() {
  return (
    <Suspense fallback={<p className="muted">loading…</p>}>
      <TasksView />
    </Suspense>
  );
}
