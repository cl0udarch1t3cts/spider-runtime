"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { StatusBadge } from "@/components/status-badge";
import { ago, isLive, sha, type DoctorTask } from "@/lib/types";

function TasksView() {
  const { data, error } = useOverview();
  const initialStatus = useSearchParams().get("status");
  const [status, setStatus] = useState<string | null>(initialStatus);
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
        const query = status ? `?status=${encodeURIComponent(status)}` : "";
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
  }, [status]);

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
            {Object.entries(counts).map(([name, count]) => (
              <button
                key={name}
                className={`chip ${status === name ? "active" : ""}`}
                onClick={() => setStatus(status === name ? null : name)}
              >
                {name} <span className="chip-count">{count}</span>
              </button>
            ))}
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
                <th>candidate</th>
                <th>updated</th>
                <th>last error</th>
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
