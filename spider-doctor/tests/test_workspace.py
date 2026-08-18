import subprocess
from pathlib import Path

import pytest

from spider_doctor.workspace import GitWorkspace


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def origin(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "origin"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "AGENTS.md").write_text("rules")
    scraper = repo / "scrapers" / "example"
    scraper.mkdir(parents=True)
    (scraper / "scrape.py").write_text("def scrape(record, ctx):\n    pass\n")
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "initial")
    return repo, git(repo, "rev-parse", "HEAD")


def test_prepares_disposable_clone_at_exact_release(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")

    workspace = manager.prepare("task-1", release)

    assert git(workspace, "rev-parse", "HEAD") == release
    assert git(workspace, "status", "--porcelain") == ""


def test_validates_only_task_scoped_changes(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    scraper = workspace / "scrapers" / "example"
    scraper.mkdir(parents=True, exist_ok=True)
    (scraper / "new.py").write_text("pass\n")

    assert manager.validate_changes(workspace, "example") == ["scrapers/example/new.py"]

    (workspace / "pyproject.toml").write_text("malicious")
    with pytest.raises(ValueError, match="outside the Doctor allowlist"):
        manager.validate_changes(workspace, "example")


def test_rejects_fixture_for_unrelated_slug(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    fixtures = workspace / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "other-place_home.html").write_text("unrelated")

    with pytest.raises(ValueError, match="outside the Doctor allowlist"):
        manager.validate_changes(workspace, "example")


def test_accepts_fixture_scoped_to_task_slug(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    fixtures = workspace / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "example_home.html").write_text("scoped")

    assert manager.validate_changes(workspace, "example") == ["tests/fixtures/example_home.html"]


def test_rejects_workspace_whose_head_changed_after_prepare(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "changed").write_text("commit")
    git(workspace, "add", "changed")
    git(
        workspace,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-qm",
        "tamper",
    )

    with pytest.raises(ValueError, match="HEAD changed"):
        manager.validate_changes(workspace, "example")


def test_accepts_unstaged_modification_of_tracked_scraper(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "scrapers" / "example" / "scrape.py").write_text(
        "def scrape(record, ctx):\n    record.set('NAME', 'Example', source=ctx.url)\n"
    )

    assert manager.validate_changes(workspace, "example") == ["scrapers/example/scrape.py"]
