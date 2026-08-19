from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pymongo.database import Database

from spider_doctor.models import DoctorTask


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


class MongoEvidenceLoader:
    def __init__(self, db: Database) -> None:
        self.db = db

    def load(self, task: DoctorTask) -> dict:
        entry = self.db.entries.find_one({"entry_id": task.entry_id})
        if entry is None:
            raise ValueError(f"entry {task.entry_id!r} is missing")
        if not str(entry.get("businessname", "")).strip() or not str(entry.get("address", "")).strip():
            raise ValueError("authoritative entry is missing businessname or address")
        if task.type == "create":
            release = task.base_release
            if not isinstance(release, str) or len(release) != 40:
                raise ValueError("create task does not contain an immutable base release")
            return _jsonable(
                {
                    "task": task.model_dump(mode="json", by_alias=True),
                    "entry": entry,
                    "run": None,
                    "artifact": None,
                    "scraper_release": release,
                }
            )
        if not task.source_run_id:
            raise ValueError("repair task does not reference a source run")
        run = self.db.execution_runs.find_one(
            {"_id": task.source_run_id, "entry_id": task.entry_id}
        )
        artifact = self.db.artifacts.find_one({"run_id": task.source_run_id})
        if run is None:
            raise ValueError(
                f"source run {task.source_run_id!r} is missing or belongs to another entry"
            )
        release = run.get("scraper_release")
        if not isinstance(release, str) or len(release) != 40:
            raise ValueError("source run does not contain an immutable scraper release")
        return _jsonable(
            {
                "task": task.model_dump(mode="json", by_alias=True),
                "entry": entry,
                "run": run,
                "artifact": artifact,
                "scraper_release": release,
            }
        )
