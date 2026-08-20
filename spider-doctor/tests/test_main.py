import sys
from types import SimpleNamespace

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