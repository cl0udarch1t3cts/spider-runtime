"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useOverview } from "@/components/overview-provider";
import { ago } from "@/lib/types";

const NAV = [
  { href: "/", label: "Overview" },
  { href: "/entries", label: "Entries" },
  { href: "/tasks", label: "Doctor tasks" },
  { href: "/runs", label: "Runs" },
];

export function SiteHeader() {
  const pathname = usePathname();
  const { data, error } = useOverview();
  const [note, setNote] = useState<string | null>(null);
  const paused = data?.executor.stats?.doctor_paused ?? false;
  // Optimistic override until the next poll confirms.
  const [optimisticPaused, setOptimisticPaused] = useState<boolean | null>(null);
  const shownPaused = optimisticPaused ?? paused;

  const togglePause = async () => {
    const next = !shownPaused;
    try {
      const response = await fetch("/api/doctor-control", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paused: next }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        setNote(`pause toggle failed: ${String(body?.error ?? response.status)}`);
        return;
      }
      setNote(null);
      setOptimisticPaused(next);
      setTimeout(() => setOptimisticPaused(null), 10_000);
    } catch (exc) {
      setNote(`pause toggle failed: ${String(exc)}`);
    }
  };

  return (
    <div className="header">
      <div className="brand">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/logo.svg" alt="Cloud Architects" width={30} height={30} />
        <div>
          <h1>SPIDER CONSOLE</h1>
          <span className="tagline">Cloud Architects</span>
        </div>
      </div>
      <nav className="nav">
        {NAV.map((item) => {
          const active =
            item.href === "/"
              ? pathname === "/"
              : pathname === item.href || pathname.startsWith(`${item.href}/`);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-link ${active ? "active" : ""}`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="header-right">
        {data?.executor.stats ? (
          <button
            className={`action pause ${shownPaused ? "paused" : ""}`}
            title={
              shownPaused
                ? "LLM calls are paused: the Doctor claims no tasks. Click to resume."
                : "Pause all LLM calls: the Doctor stops claiming tasks (in-flight runs finish)."
            }
            onClick={togglePause}
          >
            {shownPaused ? "▶ resume LLM" : "⏸ pause LLM"}
          </button>
        ) : null}
        <span className="meta">
          {data ? `refreshed ${ago(data.generatedAt)}` : "loading…"}
          {error ? <span className="error"> — {error}</span> : null}
          {note ? <span className="error"> — {note}</span> : null}
        </span>
      </div>
    </div>
  );
}
