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


def test_prepare_uses_a_blobless_partial_clone(tmp_path: Path) -> None:
    source, _ = origin(tmp_path)
    # A second commit whose blob the workspace must never need to copy.
    (source / "scrapers" / "example" / "meta.json").write_text("{}\n")
    git(source, "add", ".")
    git(source, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "second")
    first_release = git(source, "rev-parse", "HEAD~1")
    manager = GitWorkspace(source, tmp_path / "work")

    workspace = manager.prepare("task-1", first_release)

    assert git(workspace, "config", "remote.origin.partialclonefilter") == "blob:none"
    assert git(workspace, "config", "remote.origin.promisor") == "true"
    assert git(workspace, "rev-parse", "HEAD") == first_release
    # The full commit graph is present for merge-base/rebase computations.
    assert git(workspace, "rev-list", "--count", "--all") == "2"


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


def test_discards_content_dumps_inside_the_scraper_directory(tmp_path: Path) -> None:
    # Hermes saves working copies of fetched pages next to the scraper;
    # only code (.py) and metadata (.json) belong in scrapers/<entry_id>.
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    scraper = workspace / "scrapers" / "example"
    (scraper / "new.py").write_text("pass\n")
    (scraper / "meta.json").write_text("{}\n")
    (scraper / "angebot.html").write_text("<html>page dump</html>")
    (scraper / "_write_probe.txt").write_text("probe")

    changed = manager.validate_changes(workspace, "example")

    assert sorted(changed) == ["scrapers/example/meta.json", "scrapers/example/new.py"]
    assert not (scraper / "angebot.html").exists()
    assert not (scraper / "_write_probe.txt").exists()


def test_rejects_tracked_non_code_changes_inside_the_scraper_directory(tmp_path: Path) -> None:
    source, release = origin(tmp_path)
    # A tracked HTML file (from the pre-gate era) that Hermes modifies must
    # fail validation, not silently publish.
    scraper = source / "scrapers" / "example"
    (scraper / "cached.html").write_text("<html>old dump</html>")
    git(source, "add", ".")
    git(source, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "dump")
    release = git(source, "rev-parse", "HEAD")
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    (workspace / "scrapers" / "example" / "cached.html").write_text("<html>edited</html>")

    with pytest.raises(ValueError, match="outside the Doctor allowlist"):
        manager.validate_changes(workspace, "example")


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


@pytest.mark.parametrize(
    "entry_id",
    ["8_bWr7 3tjEHrLq2WsIpWHw", "-6tlhQ5q6U9tq4xVLNAIkg", "_G66OOCKSeOjO2JWkr6aNA"],
)
def test_accepts_base64url_style_upstream_entry_ids(tmp_path: Path, entry_id: str) -> None:
    source, release = origin(tmp_path)
    manager = GitWorkspace(source, tmp_path / "work")
    workspace = manager.prepare("task-1", release)
    scraper = workspace / "scrapers" / entry_id
    scraper.mkdir(parents=True)
    (scraper / "scrape.py").write_text("pass\n")

    assert manager.validate_changes(workspace, entry_id) == [f"scrapers/{entry_id}/scrape.py"]


@pytest.mark.parametrize(
    "entry_id",
    ["../escape", "/absolute", "bad/name", ".hidden", " leading-space", "trailing-space ", "x" * 129],
)
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


def test_concurrent_candidates_merge_shared_tracking_files(tmp_path: Path) -> None:
    from spider_doctor.publisher import TrustedGitPublisher

    remote = tmp_path / "remote.git"
    git(tmp_path, "init", "--bare", "-q", str(remote))
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    seed = tmp_path / "seed"
    git(tmp_path, "clone", "-q", str(remote), str(seed))
    (seed / "AGENTS.md").write_text("rules\n")
    (seed / "PROGRESS.md").write_text("# Progress\n- base note\n")
    (seed / "registry.json").write_text('{\n  "schema_version": 1,\n  "entries": []\n}\n')
    git(seed, "add", ".")
    git(seed, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "base")
    git(seed, "push", "-q", "origin", "HEAD:main")
    release = git(seed, "rev-parse", "HEAD")
    manager = GitWorkspace(seed, tmp_path / "work")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="d@example.com")

    def build(task_id: str, entry_id: str) -> tuple[Path, str]:
        workspace = manager.prepare(task_id, release)
        scraper = workspace / "scrapers" / entry_id
        scraper.mkdir(parents=True, exist_ok=True)
        (scraper / "scrape.py").write_text("pass\n")
        progress = workspace / "PROGRESS.md"
        progress.write_text(progress.read_text() + f"- {entry_id} done\n")
        registry = workspace / "registry.json"
        registry.write_text(
            f'{{\n  "schema_version": 1,\n  "entries": [{{"entry_id": "{entry_id}"}}]\n}}\n'
        )
        changed = manager.validate_changes(workspace, entry_id)
        return workspace, publisher.create_candidate(workspace, changed, f"create {entry_id}")

    ws_a, candidate_a = build("task-a", "EntryA")
    ws_b, candidate_b = build("task-b", "EntryB")
    publisher.publish(ws_a, candidate_a)
    published_b = publisher.publish(ws_b, candidate_b)

    assert git(remote, "rev-parse", "refs/heads/main") == published_b
    progress = git(remote, "show", "main:PROGRESS.md")
    assert "- EntryA done" in progress and "- EntryB done" in progress
    import json

    registry = json.loads(git(remote, "show", "main:registry.json"))
    assert {e["entry_id"] for e in registry["entries"]} == {"EntryA", "EntryB"}
