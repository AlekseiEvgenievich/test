import sys
import csv
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from task import build_table, main 


def write_csv(path: Path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "position", "performance"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def test_build_table_single_file_single_position(tmp_path):
    rows = [
        {"name": "Alice", "position": "p1", "performance": "1.0"},
        {"name": "Bob",   "position": "p1", "performance": "3.0"},
    ]

    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, rows)

    table = build_table([str(csv_path)])

    assert table == [["p1", 2.0]]


def test_build_table_multiple_positions_sorted(tmp_path):
    rows = [
        {"name": "A", "position": "p1", "performance": "2.0"},
        {"name": "B", "position": "p2", "performance": "5.0"},
        {"name": "C", "position": "p1", "performance": "4.0"},
    ]

    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, rows)

    table = build_table([str(csv_path)])

    assert table == [
        ["p2", 5.0],
        ["p1", 3.0],
    ]


def test_build_table_multiple_files_merge(tmp_path):
    rows1 = [
        {"name": "A", "position": "p1", "performance": "1.0"},
        {"name": "B", "position": "p2", "performance": "2.0"},
    ]
    rows2 = [
        {"name": "C", "position": "p1", "performance": "3.0"},
        {"name": "D", "position": "p2", "performance": "4.0"},
    ]

    csv1 = tmp_path / "data1.csv"
    csv2 = tmp_path / "data2.csv"
    write_csv(csv1, rows1)
    write_csv(csv2, rows2)

    table = build_table([str(csv1), str(csv2)])

    assert table == [
        ["p2", 3.0],
        ["p1", 2.0],
    ]


def test_build_table_rounding(tmp_path):
    rows = [
        {"name": "A", "position": "p1", "performance": "1.11"},
        {"name": "B", "position": "p1", "performance": "1.12"},
    ]

    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, rows)

    table = build_table([str(csv_path)])

    assert table == [["p1", 1.12]]


def test_main_cli_output(tmp_path, capsys, monkeypatch):
    rows = [
        {"name": "A", "position": "p1", "performance": "2.0"},
        {"name": "B", "position": "p2", "performance": "5.0"},
        {"name": "C", "position": "p1", "performance": "4.0"},
    ]

    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, rows)

    monkeypatch.setattr(
        sys,
        "argv",
        ["task.py", "--files", str(csv_path), "--report", "avg"],
    )

    main()

    captured = capsys.readouterr()
    out = captured.out

    assert "position" in out
    assert "avg" in out

    assert "p2" in out
    assert "5" in out
    assert "p1" in out
    assert "3" in out

    idx_p2 = out.index("p2")
    idx_p1 = out.index("p1")
    assert idx_p2 < idx_p1

