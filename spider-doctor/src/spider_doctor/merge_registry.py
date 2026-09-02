"""Structural git merge driver for registry.json.

Concurrent Doctor tasks each add their own entry to the shared registry;
textual merges conflict on adjacent appends. This driver unions the
``entries`` lists by identity key instead. Invoked by git as::

    <python> -m spider_doctor.merge_registry %O %A %B

where %O is the merge base, %A the current side (rebase target — written
in place with the result) and %B the other side (the candidate). A
non-zero exit reports a real conflict and falls back to git's default
behaviour.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_IDENTITY_KEYS = ("entry_id", "slug", "name")


def _identity(entry: object) -> str | None:
    if not isinstance(entry, dict):
        return None
    for key in _IDENTITY_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value:
            return f"{key}:{value}"
    return None


def merge(base: dict, ours: dict, theirs: dict) -> dict:
    merged: dict = {}
    for key in {*ours, *theirs}:
        if key == "entries":
            continue
        # A side that diverged from the base wins; on a tie ours stands.
        if key in ours and ours.get(key) == base.get(key) and key in theirs:
            merged[key] = theirs[key]
        elif key in ours:
            merged[key] = ours[key]
        else:
            merged[key] = theirs[key]
    entries: list = []
    index: dict[str, int] = {}
    for entry in [*ours.get("entries", []), *theirs.get("entries", [])]:
        identity = _identity(entry)
        if identity is None:
            if entry not in entries:
                entries.append(entry)
            continue
        if identity in index:
            entries[index[identity]] = entry
        else:
            index[identity] = len(entries)
            entries.append(entry)
    merged["entries"] = entries
    return merged


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        return 1
    try:
        base_path, ours_path, theirs_path = (Path(p) for p in argv)
        base = json.loads(base_path.read_text() or "{}")
        ours = json.loads(ours_path.read_text())
        theirs = json.loads(theirs_path.read_text())
        if not all(isinstance(d, dict) for d in (base, ours, theirs)):
            return 1
        ours_path.write_text(json.dumps(merge(base, ours, theirs), indent=2) + "\n")
    except (OSError, ValueError):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
