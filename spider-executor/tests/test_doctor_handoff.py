import mongomock
import pytest

from spider_executor.service import MongoControlService

COMMIT_SHA = "a" * 40


def test_succeeded_doctor_task_handoff_updates_revision_and_schedules_execution() -> None:
    provisioned = []
    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
        provisioner=provisioned.append,
    )
    service.ensure_indexes()
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "result": {
                    "commit_sha": COMMIT_SHA,
                    "metadata": {
                        "website": "https://example.com/contact",
                        "extracted_fields": ["NAME", "DESCRIPTION"],
                        "null_fields": ["EMAIL", "OPENING_HOURS"],
                    },
                },
            }
        },
    )

    first = service.consume_doctor_handoff(registration["task_id"])
    second = service.consume_doctor_handoff(registration["task_id"])

    assert first is not None
    assert second is not None
    assert first.id == second.id
    assert first.entry_id == "business-123"
    assert first.scraper_release == COMMIT_SHA
    assert provisioned == [COMMIT_SHA]
    entry = service.get_entry("business-123")
    assert entry is not None
    assert entry.scraper_release == COMMIT_SHA
    assert entry.website == "https://example.com/contact"
    assert entry.validation.required_fields == ["NAME", "DESCRIPTION"]
    assert entry.validation.allowed_null_fields == ["EMAIL", "OPENING_HOURS"]
    assert entry.validation.minimum_non_null_fields == 2
    assert entry.validation.allowed_source_hosts == ["example.com"]
    task = service.db.doctor_tasks.find_one({"_id": registration["task_id"]})
    assert task["handoff_job_id"] == first.id
    assert service.db.execution_jobs.count_documents({"entry_id": "business-123"}) == 1


def test_provisioning_side_effect_runs_outside_mongo_transaction() -> None:
    from contextlib import contextmanager

    in_transaction = False

    @contextmanager
    def tracked_transaction():
        nonlocal in_transaction
        in_transaction = True
        try:
            yield None
        finally:
            in_transaction = False

    def provision(_release: str) -> None:
        assert not in_transaction

    service = MongoControlService(
        mongomock.MongoClient().spider,
        release_provider=lambda: "b" * 40,
        provisioner=provision,
    )
    service._transaction = tracked_transaction
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": COMMIT_SHA}}},
    )

    assert service.consume_doctor_handoff(registration["task_id"]) is not None


def test_multiple_entries_activate_independently() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    first = service.register("business-1", "First AG", "Bern")
    second = service.register("business-2", "Second AG", "Zurich")
    service.db.doctor_tasks.update_one(
        {"_id": first["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "a" * 40}}},
    )
    service.db.doctor_tasks.update_one(
        {"_id": second["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "c" * 40}}},
    )

    assert service.consume_doctor_handoff(first["task_id"]) is not None
    assert service.consume_doctor_handoff(second["task_id"]) is not None

    assert service.get_entry("business-1").scraper_release == "a" * 40
    assert service.get_entry("business-2").scraper_release == "c" * 40
    assert service.is_entry_release_activated("business-1", "a" * 40)
    assert service.is_entry_release_activated("business-2", "c" * 40)
    assert not service.is_entry_release_activated("business-2", "a" * 40)
    from spider_executor.models import ExecutionJob

    job = service.enqueue(ExecutionJob(entry_id="business-2", idempotency_key="k2"))
    assert job.scraper_release == "c" * 40


def test_legacy_singleton_activation_record_still_authorizes_its_entry() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    service.register("business-1", "First AG", "Bern")
    service.db.entries.update_one(
        {"_id": "business-1"}, {"$set": {"scraper_release": "a" * 40}}
    )
    service.db.runtime_state.insert_one(
        {"_id": "activated_entry", "entry_id": "business-1", "scraper_release": "a" * 40}
    )

    assert service.is_entry_release_activated("business-1", "a" * 40)

    service.ensure_indexes()

    # Migration moved the record to the per-entry key; authorization holds.
    assert service.db.runtime_state.find_one({"_id": "activated_entry"}) is None
    migrated = service.db.runtime_state.find_one({"_id": "activated_entry:business-1"})
    assert migrated["scraper_release"] == "a" * 40
    assert service.is_entry_release_activated("business-1", "a" * 40)


def test_next_handoff_skips_a_poison_task_and_records_the_error() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    poison = service.register("business-1", "First AG", "Bern")
    healthy = service.register("business-2", "Second AG", "Zurich")
    service.db.doctor_tasks.update_one(
        {"_id": poison["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "completed_at": "2026-01-01T00:00:00Z",
                "result": {
                    "commit_sha": "a" * 40,
                    "metadata": "not-an-object",
                },
            }
        },
    )
    service.db.doctor_tasks.update_one(
        {"_id": healthy["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "completed_at": "2026-01-02T00:00:00Z",
                "result": {"commit_sha": "c" * 40},
            }
        },
    )

    job = service.consume_next_doctor_handoff()

    assert job is not None
    assert job.entry_id == "business-2"
    blocked = service.db.doctor_tasks.find_one({"_id": poison["task_id"]})
    assert "metadata" in blocked["handoff_error"]
    assert blocked.get("handed_off_at") is None


def test_handoff_accepts_live_run_fields_metadata_shape() -> None:
    # Newer Hermes results report official_website and a live_run_fields dict
    # instead of website plus explicit extracted/null field lists.
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "result": {
                    "commit_sha": COMMIT_SHA,
                    "metadata": {
                        "entry_id": "business-123",
                        "official_website": "https://example.com/",
                        "live_run_fields": {
                            "NAME": "Example",
                            "EMAIL": None,
                            "OPENING_HOURS": {"Mon": "09:00 - 17:00"},
                            "JOBS": None,
                        },
                    },
                },
            }
        },
    )

    assert service.consume_doctor_handoff(registration["task_id"]) is not None

    entry = service.get_entry("business-123")
    assert entry.scraper_release == COMMIT_SHA
    assert entry.website == "https://example.com/"
    assert entry.validation.required_fields == ["NAME", "OPENING_HOURS"]
    assert entry.validation.allowed_null_fields == ["EMAIL", "JOBS"]
    assert entry.validation.allowed_source_hosts == ["example.com"]
    assert service.is_entry_release_activated("business-123", COMMIT_SHA)


def test_handoff_accepts_website_only_metadata_shape() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {
            "$set": {
                "status": "succeeded",
                "result": {
                    "commit_sha": COMMIT_SHA,
                    "metadata": {
                        "entry_id": "business-123",
                        "name": "Example",
                        "website": "https://example.com/contact",
                    },
                },
            }
        },
    )

    assert service.consume_doctor_handoff(registration["task_id"]) is not None

    entry = service.get_entry("business-123")
    assert entry.scraper_release == COMMIT_SHA
    assert entry.website == "https://example.com/contact"
    # No field information available: validation expectations stay default.
    assert entry.validation.required_fields == []
    assert service.is_entry_release_activated("business-123", COMMIT_SHA)


def test_handoff_activates_despite_free_form_metadata_shapes() -> None:
    # Hermes metadata is free-form agent output; activation must never be
    # blocked by its shape. Observed variants: official_site, extracted_fields
    # without null_fields, arbitrary bookkeeping keys, no website at all.
    shapes = [
        {"entry_id": "x", "official_site": "https://example.com/", "official_name": "X"},
        {
            "entry_id": "x",
            "official_website": "https://example.com/kontakt",
            "extracted_fields": ["NAME", "EMAIL"],
        },
        {"entry_id": "x", "targeted_pytest_exit_code": 0, "live_run_exit_code": 0},
    ]
    for index, metadata in enumerate(shapes):
        service = MongoControlService(
            mongomock.MongoClient().spider, release_provider=lambda: "b" * 40
        )
        registration = service.register("business-123", "Example AG", "Bern")
        service.db.doctor_tasks.update_one(
            {"_id": registration["task_id"]},
            {
                "$set": {
                    "status": "succeeded",
                    "result": {"commit_sha": COMMIT_SHA, "metadata": metadata},
                }
            },
        )

        assert service.consume_doctor_handoff(registration["task_id"]) is not None, index

        entry = service.get_entry("business-123")
        assert entry.scraper_release == COMMIT_SHA, index
        # Incomplete field information must not create validation expectations.
        assert entry.validation.required_fields == [], index
    # The first two shapes carry a usable website.
    assert entry.website is None  # last shape had none


def test_doctor_handoff_requires_succeeded_task_with_exact_commit_sha() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")

    assert service.consume_doctor_handoff(registration["task_id"]) is None
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": "not-a-sha"}}},
    )
    assert service.consume_doctor_handoff(registration["task_id"]) is None
    assert service.db.execution_jobs.count_documents({}) == 0


def test_next_handoff_discovers_persisted_succeeded_task() -> None:
    service = MongoControlService(mongomock.MongoClient().spider, release_provider=lambda: "b" * 40)
    registration = service.register("business-123", "Example AG", "Bern")
    service.db.doctor_tasks.update_one(
        {"_id": registration["task_id"]},
        {"$set": {"status": "succeeded", "result": {"commit_sha": COMMIT_SHA}}},
    )

    job = service.consume_next_doctor_handoff()

    assert job is not None
    assert job.entry_id == "business-123"
    assert job.scraper_release == COMMIT_SHA
