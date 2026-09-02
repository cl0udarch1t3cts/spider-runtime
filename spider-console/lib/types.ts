export interface Lease {
  worker_id: string | null;
  expires_at: string | null;
}

export interface DoctorTask {
  id: string;
  entry_id: string | null;
  type: string | null;
  status: string | null;
  attempts: number;
  max_attempts: number;
  failure_class: string | null;
  last_error: string | null;
  candidate_sha: string | null;
  attempt_seconds: number | null;
  hermes_seconds: number | null;
  updated_at: string | null;
  lease: Lease | null;
}

export interface Run {
  id: string;
  entry_id: string;
  status: string;
  failure_class: string | null;
  record_id: string | null;
  scraper_release: string | null;
  failed_attempts: number | null;
  started_at: string;
  finished_at: string | null;
}

export interface EntryRow {
  id: string;
  businessname: string | null;
  website: string | null;
  active: boolean;
  scraper_release: string | null;
  updated_at: string | null;
  last_scraped_at: string | null;
}

export interface Overview {
  generatedAt: string;
  executor: {
    error?: string;
    stats?: {
      entries: number;
      records: number;
      doctor_tasks: Record<string, number>;
      execution_jobs: Record<string, number>;
      execution_runs: Record<string, number>;
      doctor_paused?: boolean;
      doctor_budget?: {
        daily_percent: number | null;
        reserve_percent: number | null;
      };
      doctor_throughput?: {
        succeeded_1h: number;
        succeeded_24h: number;
        finished_1h: number;
        finished_24h: number;
      };
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

export interface RecordField {
  value: unknown;
  source: string | null;
}

export interface ScrapedRecord {
  slug?: string;
  website?: string;
  fetched_at?: string;
  fields?: Record<string, RecordField>;
  errors?: string[];
  error?: string;
}

// The executor serializes Mongo's naive-UTC datetimes without a timezone
// suffix; parsed bare, JS reads them as local time (hence "2h ago" for a run
// that just started, on a UTC+2 machine). Treat suffix-less ISO as UTC.
export function parseUtc(iso: string): Date {
  return new Date(/[zZ]|[+-]\d{2}:?\d{2}$/.test(iso) ? iso : `${iso}Z`);
}

export function ago(iso: string | null | undefined): string {
  if (!iso) return "—";
  const seconds = Math.max(0, (Date.now() - parseUtc(iso).getTime()) / 1000);
  if (seconds < 90) return `${Math.round(seconds)}s ago`;
  if (seconds < 5400) return `${Math.round(seconds / 60)}m ago`;
  if (seconds < 129_600) return `${Math.round(seconds / 3600)}h ago`;
  return `${Math.round(seconds / 86_400)}d ago`;
}

export function duration(seconds: number | null): string {
  if (seconds === null) return "—";
  const days = Math.floor(seconds / 86_400);
  const hours = Math.floor((seconds % 86_400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return days ? `${days}d${hours}h` : `${hours}h${minutes}m`;
}

export function sha(value: string | null | undefined): string {
  return value ? value.slice(0, 10) : "—";
}

export function isLive(task: DoctorTask): boolean {
  return (
    task.status === "running" &&
    !!task.lease?.expires_at &&
    parseUtc(task.lease.expires_at).getTime() > Date.now()
  );
}

// Mongo's $group emits statuses in arbitrary, changing order; pin the
// lifecycle order so chips and counters don't reshuffle on every poll.
const STATUS_ORDER = [
  "queued",
  "running",
  "succeeded",
  "failed",
  "exhausted",
  "no_website",
  "human_review_required",
];

export function sortedStatusCounts(
  counts: Record<string, number>,
): [string, number][] {
  return Object.entries(counts).sort(([a], [b]) => {
    const ia = STATUS_ORDER.indexOf(a);
    const ib = STATUS_ORDER.indexOf(b);
    if (ia !== -1 || ib !== -1) {
      return (ia === -1 ? STATUS_ORDER.length : ia) - (ib === -1 ? STATUS_ORDER.length : ib);
    }
    return a.localeCompare(b);
  });
}

export function fieldText(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 1);
}

export function formatSeconds(s: number): string {
  if (s < 10) return `${s.toFixed(1)}s`;
  if (s < 90) return `${Math.round(s)}s`;
  return `${Math.floor(s / 60)}m ${Math.round(s % 60)}s`;
}

// Claiming a task is the only write that touches updated_at while an attempt
// is in flight, so it doubles as the attempt start for live tasks.
export function taskDuration(task: DoctorTask): string {
  if (isLive(task) && task.updated_at) {
    const s = (Date.now() - parseUtc(task.updated_at).getTime()) / 1000;
    return s >= 0 ? `${formatSeconds(s)}…` : "—";
  }
  if (task.attempt_seconds !== null && task.attempt_seconds !== undefined) {
    return formatSeconds(task.attempt_seconds);
  }
  return "—";
}

export function runDuration(
  started: string | null | undefined,
  finished: string | null | undefined,
): string {
  if (!started) return "—";
  if (!finished) return "running…";
  const ms = parseUtc(finished).getTime() - parseUtc(started).getTime();
  if (ms < 0) return "—";
  const s = ms / 1000;
  return s < 10 ? `${s.toFixed(1)}s` : `${Math.round(s)}s`;
}
