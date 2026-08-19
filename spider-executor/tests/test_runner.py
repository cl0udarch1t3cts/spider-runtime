import json
import subprocess
import sys
from pathlib import Path

from spider_executor.artifacts import LocalArtifactStore
from spider_executor.runner import SpiderRunner


def init_git(scripts: Path) -> str:
    subprocess.run(["git", "init", "-q"], cwd=scripts, check=True)
    subprocess.run(["git", "add", "."], cwd=scripts, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "initial"],
        cwd=scripts,
        check=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=scripts, text=True, capture_output=True, check=True
    ).stdout.strip()


def test_runner_executes_core_run_and_stores_output(tmp_path: Path) -> None:
    scripts = tmp_path / "spider-scripts"
    (scripts / "core").mkdir(parents=True)
    (scripts / "core" / "__init__.py").write_text("")
    (scripts / "core" / "run.py").write_text(
        "import json, sys; assert sys.argv[1:] == ['--entry-id', 'example']; "
        "print(json.dumps({'entry_id':'example','website':'https://example.com','fields':{'NAME':{'value':'Example','source':'https://example.com'}},'errors':[]}))"
    )
    init_git(scripts)
    store = LocalArtifactStore(tmp_path / "artifacts")
    runner = SpiderRunner(scripts, store, python_executable=sys.executable)

    result = runner.run("example", "run-1")

    assert result.exit_code == 0
    assert result.record.entry_id == "example"
    assert store.get(result.output_artifact.key) == json.dumps(result.record.model_dump(mode="json"), indent=2).encode()


def test_runner_converts_timeout_to_structured_failure(tmp_path: Path) -> None:
    scripts = tmp_path / "spider-scripts"
    (scripts / "core").mkdir(parents=True)
    (scripts / "core" / "__init__.py").write_text("")
    (scripts / "core" / "run.py").write_text("import time; time.sleep(2)")
    init_git(scripts)
    runner = SpiderRunner(
        scripts,
        LocalArtifactStore(tmp_path / "artifacts"),
        python_executable=sys.executable,
        timeout_seconds=0.01,
    )

    result = runner.run("example", "timeout-run")

    assert result.exit_code == 124
    assert result.failure_class.value == "SANDBOX_TIMEOUT"
    assert "timed out" in result.record.errors[0]


def test_runner_rejects_dirty_checkout_without_executing(tmp_path: Path) -> None:
    scripts = tmp_path / "spider-scripts"
    (scripts / "core").mkdir(parents=True)
    (scripts / "core" / "__init__.py").write_text("")
    marker = tmp_path / "executed"
    (scripts / "core" / "run.py").write_text(f"from pathlib import Path; Path({str(marker)!r}).write_text('yes')")
    subprocess.run(["git", "init", "-q"], cwd=scripts, check=True)
    subprocess.run(["git", "add", "."], cwd=scripts, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "initial"],
        cwd=scripts,
        check=True,
    )
    (scripts / "core" / "run.py").write_text("raise RuntimeError('dirty')")

    result = SpiderRunner(
        scripts, LocalArtifactStore(tmp_path / "artifacts"), python_executable=sys.executable
    ).run("example", "dirty-run")

    assert result.failure_class.value == "OUTPUT_SCHEMA_FAILURE"
    assert not marker.exists()


def test_runner_reports_exact_git_release(tmp_path: Path) -> None:
    scripts = tmp_path / "spider-scripts"
    (scripts / "core").mkdir(parents=True)
    (scripts / "core" / "__init__.py").write_text("")
    (scripts / "core" / "run.py").write_text(
        "import json; print(json.dumps({'entry_id':'example','fields':{},'errors':[]}))"
    )
    expected = init_git(scripts)

    result = SpiderRunner(
        scripts, LocalArtifactStore(tmp_path / "artifacts"), python_executable=sys.executable
    ).run("example", "run-1")

    assert result.scraper_release == expected
