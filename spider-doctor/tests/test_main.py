import sys
import threading
from types import SimpleNamespace

import pytest

from spider_doctor import main as doctor_main


def test_main_reconciles_orphans_before_claiming(monkeypatch) -> None:
    events = []

    class FakeLauncher:
        def reconcile_orphans(self):
            events.append("reconcile")

    class FakeWorker:
        launcher = FakeLauncher()

        def process_one(self):
            events.append("claim")

    monkeypatch.setattr(doctor_main, "Settings", lambda: SimpleNamespace(poll_seconds=0))
    monkeypatch.setattr(doctor_main, "create_worker", lambda _settings: FakeWorker())
    monkeypatch.setattr(doctor_main.signal, "signal", lambda *_args: events.append("handler"))
    monkeypatch.setattr(sys, "argv", ["spider-doctor-worker", "--once"])

    doctor_main.main()

    assert events == ["handler", "reconcile", "claim"]


def test_run_forever_processes_tasks_in_parallel() -> None:
    barrier = threading.Barrier(2, timeout=10)
    overlapped = threading.Event()

    class OverlappingWorker:
        def __init__(self):
            self.calls = 0
            self.lock = threading.Lock()

        def process_one(self):
            with self.lock:
                self.calls += 1
                calls = self.calls
            if calls <= 2:
                # Both first claims must be in flight at the same time.
                barrier.wait()
                overlapped.set()
                return
            raise SystemExit(0)

    settings = SimpleNamespace(max_parallel_tasks=2, poll_seconds=0)

    with pytest.raises(SystemExit):
        doctor_main._run_forever(OverlappingWorker(), settings)

    assert overlapped.is_set()


def test_run_forever_is_serial_when_parallelism_is_one() -> None:
    active = 0
    peak = 0
    lock = threading.Lock()

    class CountingWorker:
        calls = 0

        def process_one(self):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            CountingWorker.calls += 1
            with lock:
                active -= 1
            if CountingWorker.calls >= 5:
                raise SystemExit(0)

    settings = SimpleNamespace(max_parallel_tasks=1, poll_seconds=0)

    with pytest.raises(SystemExit):
        doctor_main._run_forever(CountingWorker(), settings)

    assert peak == 1