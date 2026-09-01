"use client";

// Write a query param into the address bar without adding history entries.
// Next (14.1+) syncs native history updates back into useSearchParams, so
// the URL is the single source of truth for view state.
export function replaceParam(key: string, value: string | null) {
  const url = new URL(window.location.href);
  if (value) {
    url.searchParams.set(key, value);
  } else {
    url.searchParams.delete(key);
  }
  window.history.replaceState(null, "", url);
}
