from __future__ import annotations

import json

import httpx

from spider_executor.models import Artifact, FailureClass, RunnerResult, ScrapedRecord


class HttpSpiderRunner:
    def __init__(
        self,
        base_url: str,
        *,
        client: httpx.Client | None = None,
        timeout_seconds: float = 120,
        max_response_bytes: int = 2 * 1024 * 1024,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(timeout=timeout_seconds)
        self.max_response_bytes = max_response_bytes

    @staticmethod
    def _failure(entry_id: str, message: str, failure: FailureClass) -> RunnerResult:
        return RunnerResult(
            exit_code=2,
            record=ScrapedRecord(entry_id=entry_id, fields={}, errors=[message]),
            output_artifact=Artifact(key="unpersisted", size_bytes=0, sha256="0" * 64),
            stderr=message,
            failure_class=failure,
        )

    def run(self, entry_id: str, run_id: str) -> RunnerResult:
        try:
            with self.client.stream(
                "POST", f"{self.base_url}/run", json={"entry_id": entry_id, "run_id": run_id}
            ) as response:
                response.raise_for_status()
                content = bytearray()
                for chunk in response.iter_bytes():
                    content.extend(chunk)
                    if len(content) > self.max_response_bytes:
                        return self._failure(
                            entry_id,
                            "runner response exceeded configured limit",
                            FailureClass.OUTPUT_SCHEMA_FAILURE,
                        )
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            return self._failure(entry_id, f"isolated runner unavailable: {exc}", FailureClass.NETWORK_TIMEOUT)
        except httpx.HTTPError as exc:
            return self._failure(entry_id, f"isolated runner HTTP failure: {exc}", FailureClass.UNKNOWN)
        try:
            return RunnerResult.model_validate(json.loads(content))
        except (json.JSONDecodeError, ValueError) as exc:
            return self._failure(entry_id, f"invalid isolated runner response: {exc}", FailureClass.OUTPUT_SCHEMA_FAILURE)
