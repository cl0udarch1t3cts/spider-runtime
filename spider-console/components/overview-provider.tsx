"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { Overview } from "@/lib/types";

interface OverviewState {
  data: Overview | null;
  error: string | null;
}

const OverviewContext = createContext<OverviewState>({
  data: null,
  error: null,
});

export function useOverview(): OverviewState {
  return useContext(OverviewContext);
}

// Single shared poller: every page and the header read from this context so
// the console makes one /api/overview request per interval, not one per view.
export function OverviewProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const response = await fetch("/api/overview", { cache: "no-store" });
        if (!response.ok) throw new Error(`overview returned ${response.status}`);
        const payload = (await response.json()) as Overview;
        if (!cancelled) {
          setData(payload);
          setError(null);
        }
      } catch (exc) {
        if (!cancelled) setError(String(exc));
      }
    };
    load();
    const timer = setInterval(load, 5000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  return (
    <OverviewContext.Provider value={{ data, error }}>
      {children}
    </OverviewContext.Provider>
  );
}
