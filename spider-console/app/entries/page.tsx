"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useMemo, useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { ago, sha, type EntryRow } from "@/lib/types";
import { replaceParam } from "@/lib/url-state";

type Filter = "all" | "active" | "inactive" | "no-scraper";

const FILTERS: { key: Filter; label: string }[] = [
  { key: "all", label: "all" },
  { key: "active", label: "active" },
  { key: "inactive", label: "inactive" },
  { key: "no-scraper", label: "no scraper yet" },
];

function matchesFilter(entry: EntryRow, filter: Filter): boolean {
  switch (filter) {
    case "active":
      return entry.active;
    case "inactive":
      return !entry.active && !!entry.scraper_release;
    case "no-scraper":
      return !entry.scraper_release;
    default:
      return true;
  }
}

function EntriesView() {
  const router = useRouter();
  const { data, error } = useOverview();
  const params = useSearchParams();
  const query = params.get("q") ?? "";
  const filterParam = params.get("filter") as Filter | null;
  const filter: Filter = FILTERS.some((f) => f.key === filterParam)
    ? (filterParam as Filter)
    : "all";
  const setQuery = (value: string) => replaceParam("q", value || null);
  const setFilter = (value: Filter) =>
    replaceParam("filter", value === "all" ? null : value);
  const [fetchNote, setFetchNote] = useState<string | null>(null);

  const entries = useMemo(() => data?.executor.entries ?? [], [data]);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return entries.filter((entry) => {
      if (!matchesFilter(entry, filter)) return false;
      if (!needle) return true;
      return (
        entry.id.toLowerCase().includes(needle) ||
        (entry.businessname ?? "").toLowerCase().includes(needle) ||
        (entry.website ?? "").toLowerCase().includes(needle)
      );
    });
  }, [entries, query, filter]);

  const triggerFetch = async (entryId: string) => {
    setFetchNote(`enqueueing ${entryId}…`);
    try {
      const response = await fetch("/api/refresh", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entryId }),
      });
      const body = await response.json().catch(() => null);
      if (response.ok) {
        setFetchNote(
          `job ${String(body?.id ?? "").slice(0, 12)} queued for ${entryId} — open the entry to watch the run`,
        );
      } else {
        setFetchNote(
          `${entryId}: ${String(body?.detail ?? body?.error ?? `HTTP ${response.status}`)}`,
        );
      }
    } catch (exc) {
      setFetchNote(`${entryId}: ${String(exc)}`);
    }
  };

  if (!data) {
    return <p className="muted">loading{error ? ` — ${error}` : "…"}</p>;
  }

  return (
    <div className="grid">
      <section className="panel wide">
        <div className="toolbar">
          <input
            className="search"
            type="search"
            placeholder="search business, entry id, or website…"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <div className="chips">
            {FILTERS.map((item) => (
              <button
                key={item.key}
                className={`chip ${filter === item.key ? "active" : ""}`}
                onClick={() => setFilter(item.key)}
              >
                {item.label}
              </button>
            ))}
          </div>
          <span className="muted">
            {filtered.length} / {entries.length}
          </span>
        </div>
        {fetchNote ? <p className="note">{fetchNote}</p> : null}
        <div className="scroll entries">
          <table>
            <thead>
              <tr>
                <th>business</th>
                <th>website</th>
                <th>entry</th>
                <th>active</th>
                <th>release</th>
                <th title="Time since the entry record last changed: re-registration or a new scraper release being activated. Not the last scrape - see the entry's runs for that">updated</th>
                <th>actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((entry) => (
                <tr
                  key={entry.id}
                  className="clickable"
                  title="Open this entry"
                  onClick={() =>
                    router.push(`/entries/${encodeURIComponent(entry.id)}`)
                  }
                >
                  <td>{entry.businessname ?? "—"}</td>
                  <td className="muted">{entry.website ?? "—"}</td>
                  <td className="muted" title={entry.id}>
                    {entry.id}
                  </td>
                  <td>{entry.active ? "yes" : "no"}</td>
                  <td>{sha(entry.scraper_release)}</td>
                  <td>{ago(entry.updated_at)}</td>
                  <td>
                    <Link
                      className="action secondary"
                      href={`/entries/${encodeURIComponent(entry.id)}`}
                      onClick={(event) => event.stopPropagation()}
                    >
                      open
                    </Link>{" "}
                    <button
                      className="action"
                      disabled={!entry.scraper_release}
                      title={
                        entry.scraper_release
                          ? "Run the spider script now and fetch the latest data"
                          : "no activated scraper release yet (Doctor has not published a scraper)"
                      }
                      onClick={(event) => {
                        event.stopPropagation();
                        triggerFetch(entry.id);
                      }}
                    >
                      fetch
                    </button>
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

export default function EntriesPage() {
  return (
    <Suspense fallback={<p className="muted">loading…</p>}>
      <EntriesView />
    </Suspense>
  );
}
