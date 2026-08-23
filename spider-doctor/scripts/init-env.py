#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(text: str, key: str, value: str) -> str:
    updated, count = re.subn(rf"^{re.escape(key)}=.*$", f"{key}={value}", text, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"{key} is missing or duplicated in .env.example")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Create non-secret Docker deployment settings")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    destination = ROOT / ".env"
    if destination.exists() and not args.force:
        raise SystemExit(".env already exists; use --force only after reviewing it")

    socket = Path("/var/run/docker.sock")
    if not socket.exists() or not stat.S_ISSOCK(socket.stat().st_mode):
        raise SystemExit("Docker socket is unavailable")
    # spider-scripts sits next to the spider-runtime monorepo, one level above
    # this service directory; the direct-sibling fallback covers pre-monorepo
    # checkouts.
    candidates = [ROOT.parent.parent / "spider-scripts", ROOT.parent / "spider-scripts"]
    scripts = next((c for c in candidates if (c / ".git").is_dir()), None)
    if scripts is None:
        raise SystemExit(
            "spider-scripts checkout is unavailable; looked in: "
            + ", ".join(str(c) for c in candidates)
        )

    text = (ROOT / ".env.example").read_text()
    values = {
        "SPIDER_DOCTOR_HOST_ROOT": str(ROOT),
        "SPIDER_SCRIPTS_HOST_PATH": str(scripts),
        "SPIDER_DOCTOR_SSH_HOST_PATH": str(Path.home() / ".ssh"),
        "SPIDER_DOCTOR_UID": str(os.getuid()),
        "SPIDER_DOCTOR_GID": str(os.getgid()),
        "SPIDER_DOCTOR_DOCKER_GID": str(Path("/var/run/docker.sock").stat().st_gid),
    }
    for key, value in values.items():
        text = replace(text, key, value)

    destination.write_text(text)
    destination.chmod(0o600)
    print(f"Wrote reviewed non-secret settings to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
