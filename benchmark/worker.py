"""Single benchmark worker process.

The worker loads one CSV, converts the fields used by the sorting algorithms
into numeric values, runs exactly one algorithm/key combination, and prints a
JSON result.  The parent process enforces the timeout.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import tracemalloc
from pathlib import Path

# Make execution robust when invoked as: python -m benchmark.worker
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from algorithms import (  # noqa: E402
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


SORTERS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}


def load_records(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    records = []
    for row in rows:
        records.append(
            {
                "Student_ID": int(row["Student_ID"]),
                "Name": row["Name"],
                "Department": row["Department"],
                "Semester": int(row["Semester"]),
                "CGPA": float(row["CGPA"]),
                "Attendance": float(row["Attendance"]),
                "Marks": int(row["Marks"]),
            }
        )
    return records


def verify_sorted(records: list[dict], key: str) -> bool:
    return all(records[i][key] <= records[i + 1][key] for i in range(len(records) - 1))


def run(path: Path, algorithm: str, key: str) -> dict:
    records = load_records(path)
    sorter = SORTERS[algorithm]

    # Dataset loading is intentionally outside the measured section. The
    # project compares sorting performance, not CSV parsing performance.
    tracemalloc.start()
    start = time.perf_counter()
    try:
        metrics = sorter(records, key)
    finally:
        elapsed = time.perf_counter() - start
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    verified = verify_sorted(records, key)
    if not verified:
        raise RuntimeError("Sorting verification failed: output is not sorted")

    return {
        "status": "COMPLETED",
        "execution_time_sec": elapsed,
        "comparisons": metrics.comparisons,
        "swaps": metrics.swaps,
        "moves": metrics.moves,
        "peak_memory_mb": peak_bytes / (1024 * 1024),
        "verified": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--algorithm", choices=sorted(SORTERS))
    parser.add_argument("--key", choices=["Student_ID", "CGPA", "Marks"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run(Path(args.file), args.algorithm, args.key)
        print(json.dumps(result))
        return 0
    except Exception as exc:  # parent turns this into a failed benchmark row
        print(
            json.dumps(
                {
                    "status": "ERROR",
                    "execution_time_sec": "",
                    "comparisons": "",
                    "swaps": "",
                    "moves": "",
                    "peak_memory_mb": "",
                    "verified": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
