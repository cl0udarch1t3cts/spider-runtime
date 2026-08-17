from pathlib import Path

import pytest

from spider_executor.artifacts import LocalArtifactStore


def test_put_writes_content_and_returns_metadata(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    artifact = store.put("runs/run-1/output.json", b'{"ok": true}')

    assert store.get(artifact.key) == b'{"ok": true}'
    assert artifact.size_bytes == 12
    assert len(artifact.sha256) == 64
    assert (tmp_path / artifact.key).is_file()


def test_put_rejects_path_traversal(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    with pytest.raises(ValueError, match="unsafe artifact key"):
        store.put("../secret", b"no")
