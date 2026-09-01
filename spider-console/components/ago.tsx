"use client";

import { ago, parseUtc } from "@/lib/types";

// Relative time with the absolute local timestamp in the hover tooltip.
export function Ago({ iso }: { iso: string | null | undefined }) {
  if (!iso) return <>—</>;
  const date = parseUtc(iso);
  return (
    <span
      title={date.toLocaleString(undefined, {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })}
    >
      {ago(iso)}
    </span>
  );
}
