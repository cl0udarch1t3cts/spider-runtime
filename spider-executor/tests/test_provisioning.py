from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from spider_executor.runtime import provision_scripts


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def test_provision_scripts_fast_forwards_clean_runtime_checkout(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    runtime = tmp_path / "runtime"
    subprocess.run(["git", "clone", "-q", str(remote), str(runtime)], check=True)
    (runtime / "base.txt").write_text("base")
    git(runtime, "add", ".")
    git(runtime, "-c", "user.name=T", "-c", "user.email=t@example.test", "commit", "-m", "base")
    git(runtime, "push", "origin", "HEAD:main")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")

    doctor = tmp_path / "doctor"
    subprocess.run(["git", "clone", "-q", str(remote), str(doctor)], check=True)
    (doctor / "scraper.txt").write_text("ready")
    git(doctor, "add", ".")
    git(doctor, "-c", "user.name=D", "-c", "user.email=d@example.test", "commit", "-m", "doctor")
    git(doctor, "push", "origin", "HEAD:main")
    release = git(doctor, "rev-parse", "HEAD")

    provision_scripts(runtime, release)

    assert git(runtime, "rev-parse", "HEAD") == release
    assert (runtime / "scraper.txt").read_text() == "ready"



def test_provision_scripts_activates_exact_doctor_sha_when_branch_has_advanced(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    runtime = tmp_path / "runtime"
    subprocess.run(["git", "clone", "-q", str(remote), str(runtime)], check=True)
    (runtime / "base.txt").write_text("base")
    git(runtime, "add", ".")
    git(runtime, "-c", "user.name=T", "-c", "user.email=t@example.test", "commit", "-m", "base")
    git(runtime, "push", "origin", "HEAD:main")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")

    doctor = tmp_path / "doctor"
    subprocess.run(["git", "clone", "-q", str(remote), str(doctor)], check=True)
    (doctor / "scraper.txt").write_text("doctor")
    git(doctor, "add", ".")
    git(doctor, "-c", "user.name=D", "-c", "user.email=d@example.test", "commit", "-m", "doctor")
    git(doctor, "push", "origin", "HEAD:main")
    doctor_release = git(doctor, "rev-parse", "HEAD")
    (doctor / "later.txt").write_text("later")
    git(doctor, "add", ".")
    git(doctor, "-c", "user.name=D", "-c", "user.email=d@example.test", "commit", "-m", "later")
    git(doctor, "push", "origin", "HEAD:main")

    provision_scripts(runtime, doctor_release)

    assert git(runtime, "rev-parse", "HEAD") == doctor_release
    assert not (runtime / "later.txt").exists()



def test_provision_scripts_refuses_dirty_checkout(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    git(repository, "init", "-q")
    (repository / "tracked").write_text("clean")
    git(repository, "add", ".")
    git(repository, "-c", "user.name=T", "-c", "user.email=t@example.test", "commit", "-m", "base")
    release = git(repository, "rev-parse", "HEAD")
    (repository / "tracked").write_text("dirty")

    with pytest.raises(RuntimeError, match="dirty"):
        provision_scripts(repository, release)


def test_provision_scripts_accepts_release_already_contained_in_checkout(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    runtime = tmp_path / "runtime"
    subprocess.run(["git", "clone", "-q", str(remote), str(runtime)], check=True)
    (runtime / "base.txt").write_text("base")
    git(runtime, "add", ".")
    git(runtime, "-c", "user.name=T", "-c", "user.email=t@example.test", "commit", "-m", "base")
    older = git(runtime, "rev-parse", "HEAD")
    (runtime / "next.txt").write_text("next")
    git(runtime, "add", ".")
    git(runtime, "-c", "user.name=T", "-c", "user.email=t@example.test", "commit", "-m", "next")
    tip = git(runtime, "rev-parse", "HEAD")
    git(runtime, "push", "origin", "HEAD:main")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")

    # The checkout already contains the older commit; provisioning must not
    # move backwards and must not fail.
    provision_scripts(runtime, older)

    assert git(runtime, "rev-parse", "HEAD") == tip
