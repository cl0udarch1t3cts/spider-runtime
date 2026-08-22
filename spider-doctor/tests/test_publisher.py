import subprocess
from pathlib import Path

import pytest

from spider_doctor.publisher import TrustedGitPublisher


def git(cwd: Path, *args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check, text=True, capture_output=True
    ).stdout.strip()


def repositories(tmp_path: Path) -> tuple[Path, Path]:
    remote = tmp_path / "remote.git"
    git(tmp_path, "init", "--bare", "-q", str(remote))
    workspace = tmp_path / "workspace"
    git(tmp_path, "clone", "-q", str(remote), str(workspace))
    (workspace / "AGENTS.md").write_text("rules\n")
    git(workspace, "add", "AGENTS.md")
    git(workspace, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "base")
    git(workspace, "push", "-q", "origin", "HEAD:main")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    return workspace, remote


def test_trusted_publisher_commits_and_pushes_only_validated_files(tmp_path: Path) -> None:
    workspace, remote = repositories(tmp_path)
    scraper = workspace / "scrapers" / "Entry_1"
    scraper.mkdir(parents=True)
    changed = scraper / "scrape.py"
    changed.write_text("pass\n")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="doctor@example.com")

    candidate = publisher.create_candidate(
        workspace, ["scrapers/Entry_1/scrape.py"], "Doctor create Entry_1"
    )
    publisher.publish(workspace, candidate)

    assert git(remote, "rev-parse", "refs/heads/main") == candidate
    assert git(workspace, "show", "--pretty=", "--name-only", candidate) == "scrapers/Entry_1/scrape.py"


def test_candidate_creation_fails_if_validated_list_omits_a_change(tmp_path: Path) -> None:
    workspace, _ = repositories(tmp_path)
    (workspace / "allowed").write_text("ok")
    (workspace / "unvalidated").write_text("bad")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="doctor@example.com")

    with pytest.raises(ValueError, match="validated files do not exactly match"):
        publisher.create_candidate(workspace, ["allowed"], "Doctor repair Entry_1")


def advance_remote(tmp_path: Path, remote: Path, filename: str, content: str) -> None:
    other = tmp_path / f"other-{filename}"
    git(tmp_path, "clone", "-q", str(remote), str(other))
    (other / filename).write_text(content)
    git(other, "add", filename)
    git(other, "-c", "user.name=Other", "-c", "user.email=other@example.com", "commit", "-qm", "concurrent")
    git(other, "push", "-q", "origin", "HEAD:main")


def test_publish_rebases_stale_candidate_onto_advanced_remote(tmp_path: Path) -> None:
    workspace, remote = repositories(tmp_path)
    scraper = workspace / "scrapers" / "Entry_1"
    scraper.mkdir(parents=True)
    (scraper / "scrape.py").write_text("pass\n")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="doctor@example.com")
    candidate = publisher.create_candidate(workspace, ["scrapers/Entry_1/scrape.py"], "Doctor create Entry_1")
    advance_remote(tmp_path, remote, "concurrent.txt", "someone else won the race\n")

    published = publisher.publish(workspace, candidate)

    assert published != candidate
    assert git(remote, "rev-parse", "refs/heads/main") == published
    assert git(workspace, "show", f"{published}:scrapers/Entry_1/scrape.py") == "pass"
    assert git(workspace, "show", f"{published}:concurrent.txt") == "someone else won the race"


def test_publish_conflicting_rebase_fails_and_restores_candidate(tmp_path: Path) -> None:
    workspace, remote = repositories(tmp_path)
    (workspace / "AGENTS.md").write_text("candidate version\n")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="doctor@example.com")
    candidate = publisher.create_candidate(workspace, ["AGENTS.md"], "Doctor repair Entry_1")
    advance_remote(tmp_path, remote, "AGENTS.md", "conflicting concurrent version\n")

    with pytest.raises(RuntimeError, match="could not be rebased"):
        publisher.publish(workspace, candidate)

    assert git(workspace, "rev-parse", "HEAD") == candidate
    assert git(workspace, "status", "--porcelain") == ""


def test_reconciliation_accepts_candidate_contained_in_later_remote_tip(tmp_path: Path) -> None:
    workspace, _ = repositories(tmp_path)
    (workspace / "first").write_text("one")
    publisher = TrustedGitPublisher(branch="main", author_name="Doctor", author_email="doctor@example.com")
    candidate = publisher.create_candidate(workspace, ["first"], "candidate")
    publisher.publish(workspace, candidate)
    (workspace / "later").write_text("two")
    git(workspace, "add", "later")
    git(workspace, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "later")
    git(workspace, "push", "-q", "origin", "HEAD:main")

    assert publisher.is_published(workspace, candidate)
