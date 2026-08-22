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

    (workspace / "AGENTS.md").write_text("malicious edit of a tracked file")
    with pytest.raises(ValueError, match="outside the Doctor allowlist"):
        manager.validate_changes(workspace, "example")


def test_discards_untracked_scratch_files_outside_allowlist(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "scrapers" / "example" / "new.py").write_text("pass\n")
    scratch = workspace / ".tmp"
    scratch.mkdir()
    (scratch / "dean_ch_de.html").write_text("<html>cached page</html>")
    fixtures = workspace / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "other-place_home.html").write_text("unrelated")

    assert manager.validate_changes(workspace, "example") == ["scrapers/example/new.py"]
    assert not (scratch / "dean_ch_de.html").exists()
    assert not (fixtures / "other-place_home.html").exists()


def test_accepts_fixture_directory_scoped_to_entry_id(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    fixtures = workspace / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    owned = fixtures / "Example_1"
    owned.mkdir()
    (owned / "home.html").write_text("scoped")

    assert manager.validate_changes(workspace, "Example_1") == ["tests/fixtures/Example_1/home.html"]


def test_entry_id_uses_spider_scripts_safe_identifier_grammar(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    scraper = workspace / "scrapers" / "Entry_1.2"
    scraper.mkdir(parents=True)
    (scraper / "scrape.py").write_text("pass\n")

    assert manager.validate_changes(workspace, "Entry_1.2") == ["scrapers/Entry_1.2/scrape.py"]


@pytest.mark.parametrize("entry_id", ["../escape", "/absolute", "bad/name", "-leading", "x" * 129])
def test_rejects_unsafe_entry_id(tmp_path: Path, entry_id: str) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)

    with pytest.raises(ValueError, match="unsafe entry_id"):
        manager.validate_changes(workspace, entry_id)


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


def test_resume_restores_workspace_head_to_recorded_candidate(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "scrapers" / "example" / "new.py").write_text("pass\n")
    git(workspace, "add", "scrapers/example/new.py")
    git(workspace, "-c", "user.name=T", "-c", "user.email=t@example.com", "commit", "-qm", "candidate")
    candidate = git(workspace, "rev-parse", "HEAD")
    git(workspace, "checkout", "--quiet", "--detach", release)

    resumed = manager.resume("task-1", candidate)

    assert git(resumed, "rev-parse", "HEAD") == candidate


def test_accepts_unstaged_modification_of_tracked_scraper(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "scrapers" / "example" / "scrape.py").write_text(
        "def scrape(record, ctx):\n    record.set('NAME', 'Example', source=ctx.url)\n"
    )

    assert manager.validate_changes(workspace, "example") == ["scrapers/example/scrape.py"]
