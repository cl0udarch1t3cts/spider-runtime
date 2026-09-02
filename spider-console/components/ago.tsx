"use client";

import { useSyncExternalStore } from "react";
import { ago, parseUtc } from "@/lib/types";

// One shared 1s ticker re-renders every mounted <Ago>, so relative times
// visibly age between data polls instead of freezing at "0s ago".
const subscribers = new Set<() => void>();
let timer: ReturnType<typeof setInterval> | null = null;

function subscribe(callback: () => void): () => void {
  subscribers.add(callback);
  timer ??= setInterval(() => {
    for (const notify of subscribers) notify();
  }, 1000);
  return () => {
    subscribers.delete(callback);
    if (!subscribers.size && timer) {
      clearInterval(timer);
      timer = null;
    }
  };
}

const nowSeconds = () => Math.floor(Date.now() / 1000);

// Relative time with the absolute local timestamp in the hover tooltip.
export function Ago({ iso }: { iso: string | null | undefined }) {
  useSyncExternalStore(subscribe, nowSeconds, () => 0);
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
