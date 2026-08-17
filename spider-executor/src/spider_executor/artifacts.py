from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

from spider_executor.models import Artifact


class LocalArtifactStore:
    def __init__(self, root: Path, *, max_size_bytes: int = 20 * 1024 * 1024) -> None:
        self.root = root.resolve()
        self.max_size_bytes = max_size_bytes
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        pure = PurePosixPath(key)
        if pure.is_absolute() or ".." in pure.parts or not pure.parts:
            raise ValueError(f"unsafe artifact key: {key!r}")
        path = (self.root / Path(*pure.parts)).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError(f"unsafe artifact key: {key!r}")
        return path

    def put(self, key: str, content: bytes) -> Artifact:
        if len(content) > self.max_size_bytes:
            raise ValueError("artifact exceeds configured size limit")
        destination = self._path(key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        temporary.replace(destination)
        return Artifact(
            key=key,
            size_bytes=len(content),
            sha256=hashlib.sha256(content).hexdigest(),
        )

    def get(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).is_file()

    def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)
