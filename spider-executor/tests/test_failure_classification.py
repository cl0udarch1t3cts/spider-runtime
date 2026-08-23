from spider_executor.failure import classify_runner_failure
from spider_executor.models import FailureClass


def test_classifies_persistent_429_as_datacenter_block() -> None:
    failure = classify_runner_failure(
        "fetch failed: Failed to fetch after 3 attempts: 429 Client Error: Too Many Requests"
    )
    assert failure == FailureClass.HTTP_DATACENTER_BLOCK


def test_classifies_timeout_without_summoning_code_repair() -> None:
    assert classify_runner_failure("Read timed out after 20 seconds") == FailureClass.NETWORK_TIMEOUT


def test_classifies_python_traceback_as_scraper_exception() -> None:
    assert classify_runner_failure("scraper raised: Traceback (most recent call last)") == FailureClass.SCRAPER_EXCEPTION


def test_only_deterministic_failures_are_doctor_eligible() -> None:
    assert FailureClass.SCRAPER_EXCEPTION.doctor_eligible
    assert FailureClass.SEMANTIC_VALIDATION_FAILURE.doctor_eligible
    assert not FailureClass.HTTP_DATACENTER_BLOCK.doctor_eligible
    assert not FailureClass.NETWORK_TIMEOUT.doctor_eligible
