import mongomock

from spider_executor.service import MongoControlService


def test_index_migration_reconciles_legacy_create_and_repair_tasks() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.db.doctor_tasks.insert_many(
        [
            {
                "_id": "create",
                "entry_id": "example",
                "type": "create",
                "active_key": "example:create",
                "status": "queued",
            },
            {
                "_id": "repair",
                "entry_id": "example",
                "type": "repair",
                "active_key": "example:repair",
                "status": "queued",
            },
        ]
    )

    service.ensure_indexes()

    create = service.db.doctor_tasks.find_one({"_id": "create"})
    repair = service.db.doctor_tasks.find_one({"_id": "repair"})
    assert create["active_key"] == "example"
    assert "active_key" not in repair
    assert repair["status"] == "human_review_required"


def test_ensure_indexes_creates_unique_operational_indexes() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.ensure_indexes()
    jobs = service.db.execution_jobs.index_information()
    doctor = service.db.doctor_tasks.index_information()
    assert jobs["idempotency_key_1"]["unique"]
    assert doctor["active_doctor_task_per_entry"]["unique"]
