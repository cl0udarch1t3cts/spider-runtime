import { readFileSync } from "node:fs";

const EXECUTOR_API_URL = (
  process.env.EXECUTOR_API_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");
const USAGE_URL = process.env.USAGE_URL ?? "";
const USAGE_TOKEN_FILE = process.env.USAGE_TOKEN_FILE ?? "";

const BUDGET_DAILY_PERCENT = Number(process.env.BUDGET_DAILY_PERCENT ?? "10");
const BUDGET_RESERVE_PERCENT = Number(process.env.BUDGET_RESERVE_PERCENT ?? "30");

export interface UsageWindow {
  name: string;
  used_percent: number;
  window_minutes: number | null;
  resets_in_seconds: number | null;
}

export interface Budget {
  usedPercent: number;
  allowedPercent: number;
  day: number | null;
  totalDays: number | null;
  resetsInSeconds: number | null;
  dailyPercent: number;
  reservePercent: number;
  decision: "proceed" | "defer";
  source: string;
}

async function executorGet<T>(path: string): Promise<T> {
  const response = await fetch(`${EXECUTOR_API_URL}${path}`, {
    cache: "no-store",
    signal: AbortSignal.timeout(10_000),
  });
  if (!response.ok) {
    throw new Error(`executor API ${path} returned ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchRecord(recordId: string) {
  return executorGet<Record<string, unknown>>(
    `/api/v1/records/${encodeURIComponent(recordId)}`,
  );
}

export async function fetchDoctorTasks(status: string | null) {
  const filter = status ? `&status=${encodeURIComponent(status)}` : "";
  return executorGet<Record<string, unknown>[]>(
    `/api/v1/doctor-tasks?limit=200${filter}`,
  );
}

export async function fetchEntryRuns(entryId: string) {
  return executorGet<Record<string, unknown>[]>(
    `/api/v1/entries/${encodeURIComponent(entryId)}/runs`,
  );
}

export async function fetchLatestRecordId(
  entryId: string,
): Promise<string | null> {
  const runs = await executorGet<
    { record_id: string | null; status: string; started_at: string }[]
  >(`/api/v1/entries/${encodeURIComponent(entryId)}/runs`);
  const latest = runs
    .filter((run) => run.status === "succeeded" && run.record_id)
    .sort((a, b) => b.started_at.localeCompare(a.started_at))[0];
  return latest?.record_id ?? null;
}

export async function enqueueExecution(entryId: string): Promise<{
  ok: boolean;
  status: number;
  body: unknown;
}> {
  const response = await fetch(`${EXECUTOR_API_URL}/api/v1/execution-jobs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ entry_id: entryId, trigger: "console" }),
    cache: "no-store",
    signal: AbortSignal.timeout(10_000),
  });
  return {
    ok: response.ok,
    status: response.status,
    body: await response.json().catch(() => null),
  };
}

export async function fetchExecutor() {
  const [stats, tasks, runs, entries] = await Promise.all([
    executorGet<Record<string, unknown>>("/api/v1/stats"),
    executorGet<Record<string, unknown>[]>("/api/v1/doctor-tasks?limit=50"),
    executorGet<Record<string, unknown>[]>("/api/v1/runs?limit=50"),
    executorGet<Record<string, unknown>[]>("/api/v1/entries"),
  ]);
  return { stats, tasks, runs, entries };
}

export async function fetchUsage(): Promise<{
  windows: UsageWindow[];
  source: string;
  budget: Budget | null;
} | null> {
  if (!USAGE_URL) return null;
  let token = "";
  try {
    token = readFileSync(USAGE_TOKEN_FILE, "utf-8").trim();
  } catch {
    return null;
  }
  const response = await fetch(USAGE_URL, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
    signal: AbortSignal.timeout(30_000),
  });
  if (!response.ok) return null;
  const payload = (await response.json()) as {
    source: string;
    windows: UsageWindow[];
  };
  return {
    ...payload,
    budget: computeBudget(payload.windows, payload.source),
  };
}

// Mirrors spider_doctor/budget.py: pace the weekly window at dailyPercent/day,
// hard-capped so reservePercent stays free for development.
export function computeBudget(
  windows: UsageWindow[],
  source: string,
): Budget | null {
  if (!windows.length) return null;
  const withDuration = windows.filter((w) => w.window_minutes);
  const weekly = withDuration.length
    ? withDuration.reduce((a, b) =>
        (a.window_minutes ?? 0) >= (b.window_minutes ?? 0) ? a : b,
      )
    : (windows.find((w) => w.name === "secondary" || w.name === "weekly") ??
      windows.reduce((a, b) => (a.used_percent >= b.used_percent ? a : b)));

  const cap = 100 - BUDGET_RESERVE_PERCENT;
  let allowed = cap;
  let day: number | null = null;
  let totalDays: number | null = null;
  if (weekly.window_minutes && weekly.resets_in_seconds !== null) {
    const windowSeconds = weekly.window_minutes * 60;
    const elapsed = Math.min(
      windowSeconds,
      Math.max(0, windowSeconds - weekly.resets_in_seconds),
    );
    totalDays = Math.max(1, Math.round(windowSeconds / 86_400));
    day = Math.min(Math.floor(elapsed / 86_400) + 1, totalDays);
    allowed = Math.min(cap, BUDGET_DAILY_PERCENT * day);
  }
  return {
    usedPercent: weekly.used_percent,
    allowedPercent: allowed,
    day,
    totalDays,
    resetsInSeconds: weekly.resets_in_seconds,
    dailyPercent: BUDGET_DAILY_PERCENT,
    reservePercent: BUDGET_RESERVE_PERCENT,
    decision: weekly.used_percent < allowed ? "proceed" : "defer",
    source,
  };
}
