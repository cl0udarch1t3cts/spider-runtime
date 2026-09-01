"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { replaceParam } from "@/lib/url-state";
import { useOverview } from "@/components/overview-provider";
import { Ago } from "@/components/ago";
import { StatusBadge } from "@/components/status-badge";
import {
  fieldText,
  sha,
  type Run,
  type ScrapedRecord,
} from "@/lib/types";

function EntryDetailView() {
  const params = useParams<{ id: string }>();
  // Entry IDs contain no "%", so decoding an already-decoded segment is safe.
  const entryId = decodeURIComponent(params.id);
  // A pinned record lives in the URL so refresh and back/forward keep it.
  const pinnedRecordId = useSearchParams().get("record");
  const pinned = pinnedRecordId !== null;

  const { data } = useOverview();
  const [runs, setRuns] = useState<Run[] | null>(null);
  const [runsError, setRunsError] = useState<string | null>(null);
  const [record, setRecord] = useState<ScrapedRecord | null>(null);
  const [fetchNote, setFetchNote] = useState<string | null>(null);

  const entry = useMemo(
    () => data?.executor.entries?.find((item) => item.id === entryId) ?? null,
    [data, entryId],
  );

  const tasks = useMemo(
    () =>
      (data?.executor.tasks ?? []).filter((task) => task.entry_id === entryId),
    [data, entryId],
  );

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch(
          `/api/entry-runs/${encodeURIComponent(entryId)}`,
          { cache: "no-store" },
        );
        const body = (await response.json()) as Run[] | { error: string };
        if (cancelled) return;
        if (Array.isArray(body)) {
          setRuns(
            [...body].sort((a, b) => b.started_at.localeCompare(a.started_at)),
          );
          setRunsError(null);
        } else {
          setRunsError(body.error);
        }
      } catch (exc) {
        if (!cancelled) setRunsError(String(exc));
      }
    };
    load();
    const timer = setInterval(load, 10_000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [entryId]);

  const latestRecordId = useMemo(
    () =>
      runs?.find((run) => run.status === "succeeded" && run.record_id)
        ?.record_id ?? null,
    [runs],
  );
  const recordId = pinnedRecordId ?? latestRecordId;

  useEffect(() => {
    if (!recordId) {
      setRecord(null);
      return;
    }
    let cancelled = false;
    fetch(`/api/record/${encodeURIComponent(recordId)}`)
      .then(async (response) => (await response.json()) as ScrapedRecord)
      .then((payload) => {
        if (!cancelled) setRecord(payload);
      })
      .catch((exc) => {
        if (!cancelled) setRecord({ error: String(exc) });
      });
    return () => {
      cancelled = true;
    };
  }, [recordId]);

  const triggerFetch = async () => {
    setFetchNote("enqueueing…");
    try {
      const response = await fetch("/api/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entryId }),
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setFetchNote(
          `job ${String(body?.id ?? "").slice(0, 12)} queued — a fresh run appears below once the worker picks it up`,
        );
      } else {
        setFetchNote(
          String(body?.detail ?? body?.error ?? `HTTP ${response.status}`),
        );
      }
    } catch (exc) {
      setFetchNote(String(exc));
    }
  };

  return (
    <div className="grid">
      <section className="panel wide">
        <p className="breadcrumb">
          <Link className="link" href="/entries">
            ← entries
          </Link>
        </p>
        <div className="entry-head">
          <div>
            <h2 className="entry-title">
              {entry?.businessname ?? entryId}
            </h2>
            <p className="muted">
              {entry?.website ? (
                <a
                  className="link"
                  href={entry.website}
                  target="_blank"
                  rel="noreferrer"
                >
                  {entry.website}
                </a>
              ) : (
                "no website yet"
              )}{" "}
              · id <span title={entryId}>{entryId}</span> ·{" "}
              {entry?.active ? "active" : "inactive"} · release{" "}
              {sha(entry?.scraper_release)} · updated <Ago iso={entry?.updated_at} />
            </p>
          </div>
          <button
            className="action"
            disabled={!entry?.scraper_release}
            title={
              entry?.scraper_release
                ? "Run the spider script now and fetch the latest data"
                : "no activated scraper release yet (Doctor has not published a scraper)"
            }
            onClick={triggerFetch}
          >
            fetch now
          </button>
        </div>
        {fetchNote ? <p className="note">{fetchNote}</p> : null}
      </section>

      <section className="panel wide">
        <h2>
          Scraped record{" "}
          {pinned ? (
            <button
              className="link"
              onClick={() => replaceParam("record", null)}
            >
              (follow latest)
            </button>
          ) : null}
        </h2>
        {record?.fields ? (
          <>
            <p className="muted">
              fetched <Ago iso={record.fetched_at ?? null} /> · record{" "}
              {recordId?.slice(0, 12)}
            </p>
            <table>
              <thead>
                <tr>
                  <th>field</th>
                  <th>value</th>
                  <th>source</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(record.fields).map(([name, field]) => (
                  <tr key={name}>
                    <td>{name}</td>
                    <td className="value-cell">{fieldText(field.value)}</td>
                    <td className="muted">{field.source ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ) : record?.error ? (
          <p className="error">{record.error}</p>
        ) : (
          <p className="muted">
            no scraped record yet — the Doctor may still be building the
            scraper, or no run has succeeded
          </p>
        )}
      </section>

      <section className="panel wide">
        <h2>Runs</h2>
        {runsError ? <p className="error">{runsError}</p> : null}
        {runs && runs.length ? (
          <div className="scroll">
            <table>
              <thead>
                <tr>
                  <th>run</th>
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
                    <td>
                      <StatusBadge value={run.status} />
                    </td>
                    <td>{run.failure_class ?? "—"}</td>
                    <td>{sha(run.scraper_release)}</td>
                    <td>
                      {run.record_id ? (
                        <button
                          className="link"
                          onClick={() => replaceParam("record", run.record_id)}
                        >
                          {run.record_id.slice(0, 12)}
                        </button>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td><Ago iso={run.started_at} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : runs ? (
          <p className="muted">no runs for this entry yet</p>
        ) : (
          <p className="muted">loading…</p>
        )}
      </section>

      {tasks.length ? (
        <section className="panel wide">
          <h2>Doctor tasks</h2>
          <div className="scroll">
            <table>
              <thead>
                <tr>
                  <th>type</th>
                  <th>status</th>
                  <th>att</th>
                  <th>candidate</th>
                  <th title="Time since the Doctor last touched this task: claimed it, finished an attempt, or changed its status">last activity</th>
                  <th title="Why the Doctor's most recent attempt failed (task-level). Script execution failures show as a run's failure class instead">last error</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id}>
                    <td>{task.type}</td>
                    <td>
                      <StatusBadge value={task.status} />
                    </td>
                    <td>
                      {task.attempts}/{task.max_attempts}
                    </td>
                    <td>{sha(task.candidate_sha)}</td>
                    <td><Ago iso={task.updated_at} /></td>
                    <td
                      className={`err-cell ${task.status === "succeeded" ? "muted" : ""}`}
                      title={task.last_error ?? ""}
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
      ) : null}
    </div>
  );
}

export default function EntryDetailPage() {
  return (
    <Suspense fallback={<p className="muted">loading…</p>}>
      <EntryDetailView />
    </Suspense>
  );
}
