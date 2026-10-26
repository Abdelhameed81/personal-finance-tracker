from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

import src.main as main_module


def test_main_reports_corrupt_data_file_and_leaves_it_untouched(
        tmp_path: Path, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    corrupt_file = tmp_path / "transactions.json"
    corrupt_text = '[{"date": "2024-10-09T14:32:00" "type": "INCOME"}]'
    corrupt_file.write_text(corrupt_text, encoding="utf-8")
    monkeypatch.setattr(main_module, "DATA_FILE", corrupt_file)

    assert main_module.main() == 1

    captured = capsys.readouterr()
    assert "corrupt or invalid" in captured.err
    assert "JSONDecodeError" in captured.err
    assert corrupt_file.read_text(encoding="utf-8") == corrupt_text


def test_main_reports_unreadable_data_file(
        tmp_path: Path, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    # A directory where the file should be: is_file() is False, so use a failing read instead
    monkeypatch.setattr(main_module, "DATA_FILE", tmp_path / "transactions.json")

    def failing_service(_repo: object) -> None:
        raise PermissionError("denied")

    monkeypatch.setattr(main_module, "TransactionService", failing_service)

    assert main_module.main() == 1
    assert "Could not read" in capsys.readouterr().err


@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError])
def test_main_exits_cleanly_on_interrupt(
        tmp_path: Path, monkeypatch: MonkeyPatch, capsys: CaptureFixture[str],
        interrupt: type[BaseException]) -> None:
    monkeypatch.setattr(main_module, "DATA_FILE", tmp_path / "transactions.json")

    def raise_interrupt(_service: object) -> None:
        raise interrupt

    monkeypatch.setattr(main_module, "run_app", raise_interrupt)

    assert main_module.main() == 0
    assert "Goodbye" in capsys.readouterr().out
