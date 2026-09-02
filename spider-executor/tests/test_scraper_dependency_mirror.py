"""Guard against scraper-dependency drift.

The runner image installs the executor's own dependency set, which
mirrors what spider-scripts' scrapers import (requests, bs4, ...).
When the framework grows a dependency (as core/pdf.py did with pypdf),
production scrapers crash on import unless the mirror keeps up — the
Doctor's containers resolve spider-scripts' deps themselves and never
notice. This test reads the sibling checkout's declared dependencies
and demands each one is mirrored here.
"""

import re
import tomllib
from pathlib import Path

import pytest

SCRIPTS_PYPROJECT = Path(__file__).resolve().parents[2].parent / "spider-scripts" / "pyproject.toml"
EXECUTOR_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def _package_names(dependencies: list[str]) -> set[str]:
    return {
        re.split(r"[<>=!~\[; ]", dependency.strip(), maxsplit=1)[0].lower()
        for dependency in dependencies
    }


@pytest.mark.skipif(
    not SCRIPTS_PYPROJECT.is_file(),
    reason="sibling spider-scripts checkout not present (CI)",
)
def test_executor_mirrors_all_scraper_runtime_dependencies() -> None:
    scripts = tomllib.loads(SCRIPTS_PYPROJECT.read_text())
    executor = tomllib.loads(EXECUTOR_PYPROJECT.read_text())

    required = _package_names(scripts["project"]["dependencies"])
    mirrored = _package_names(executor["project"]["dependencies"])

    missing = sorted(required - mirrored)
    assert not missing, (
        f"spider-scripts dependencies missing from spider-executor: {missing} — "
        "add them to spider-executor/pyproject.toml so the runner image can import them"
    )
