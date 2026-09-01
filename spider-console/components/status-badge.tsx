export function StatusBadge({ value }: { value: string | null | undefined }) {
  return <span className={`status ${value ?? ""}`}>{value ?? "—"}</span>;
}
