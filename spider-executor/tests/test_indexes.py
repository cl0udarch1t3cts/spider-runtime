import mongomock

from spider_executor.service import MongoControlService


def test_ensure_indexes_creates_unique_operational_indexes() -> None:
    service = MongoControlService(mongomock.MongoClient().spider)
    service.ensure_indexes()
    jobs = service.db.execution_jobs.index_information()
    doctor = service.db.doctor_tasks.index_information()
    assert jobs["idempotency_key_1"]["unique"]
    assert doctor["active_repair_per_slug"]["unique"]
