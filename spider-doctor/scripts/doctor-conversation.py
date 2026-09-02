#!/usr/bin/env python3
"""Print a Doctor task's Hermes conversation from its persisted state.db.

Every task home under data/tasks/<task_id>/hermes-home keeps the full
agent transcript (messages) and token accounting (sessions) in SQLite.
This reads them read-only; it never touches the broker home or OAuth.

Usage:
  doctor-conversation.py                 # list recent tasks with usage
  doctor-conversation.py <task_id>       # print that task's transcript
  doctor-conversation.py <task_id> --full  # untruncated message bodies
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parent.parent / "data" / "tasks"
SNIPPET = 160


def open_db(task_id: str) -> sqlite3.Connection:
    db = TASK_ROOT / task_id / "hermes-home" / "state.db"
    if not db.is_file():
        sys.exit(f"no state.db for task {task_id!r} under {TASK_ROOT}")
    return sqlite3.connect(f"file:{db}?mode=ro", uri=True)


def list_tasks() -> None:
    rows = []
    for db in sorted(
        TASK_ROOT.glob("*/hermes-home/state.db"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:25]:
        task_id = db.parts[-3]
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            session = con.execute(
                "SELECT message_count, api_call_count, input_tokens, output_tokens,"
                " cache_read_tokens, started_at FROM sessions LIMIT 1"
            ).fetchone()
            con.close()
        except sqlite3.Error:
            continue
        if session:
            rows.append((task_id, *session))
    print(f"{'task':38} {'msgs':>5} {'calls':>5} {'input':>10} {'output':>8} {'cached':>11}  started")
    for task_id, msgs, calls, tin, tout, cached, started in rows:
        print(
            f"{task_id:38} {msgs or 0:>5} {calls or 0:>5} {tin or 0:>10,}"
            f" {tout or 0:>8,} {cached or 0:>11,}  {started or '—'}"
        )


def show_task(task_id: str, full: bool) -> None:
    con = open_db(task_id)
    session = con.execute(
        "SELECT model, message_count, api_call_count, input_tokens, output_tokens,"
        " cache_read_tokens, reasoning_tokens, started_at, ended_at, end_reason"
        " FROM sessions LIMIT 1"
    ).fetchone()
    if session:
        model, msgs, calls, tin, tout, cached, reason_toks, started, ended, end_reason = session
        print(f"task {task_id}")
        print(f"model={model} messages={msgs} api_calls={calls} started={started} ended={ended} ({end_reason})")
        print(
            f"tokens: input={tin or 0:,} output={tout or 0:,}"
            f" cache_read={cached or 0:,} reasoning={reason_toks or 0:,}"
        )
        print("-" * 100)
    for role, tool, content, ts in con.execute(
        "SELECT role, tool_name, coalesce(content, ''), timestamp FROM messages ORDER BY id"
    ):
        label = f"{role}/{tool}" if tool else role
        body = content if full else content[:SNIPPET].replace("\n", " ")
        suffix = "" if full or len(content) <= SNIPPET else f" …[{len(content):,} chars]"
        print(f"[{ts}] {label:24} {body}{suffix}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_id", nargs="?", help="Doctor task id; omit to list recent tasks")
    parser.add_argument("--full", action="store_true", help="print untruncated message bodies")
    args = parser.parse_args()
    if args.task_id:
        show_task(args.task_id, args.full)
    else:
        list_tasks()


if __name__ == "__main__":
    main()
