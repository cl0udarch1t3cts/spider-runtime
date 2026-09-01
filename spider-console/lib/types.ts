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

export function ago(iso: string | null | undefined): string {
  if (!iso) return "—";
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
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
    new Date(task.lease.expires_at).getTime() > Date.now()
  );
}

export function fieldText(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 1);
}
