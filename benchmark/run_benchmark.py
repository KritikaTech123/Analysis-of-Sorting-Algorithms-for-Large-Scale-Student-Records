"""Run reproducible sorting benchmarks across datasets.

The runner executes each algorithm in a separate process so an intentionally
slow O(n^2) experiment can be stopped without killing the complete benchmark.
Results are written to a structured CSV as required by the PBL plan.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ALGORITHMS = ("bubble", "selection", "insertion", "merge", "quick")
CONDITIONS = ("random", "sorted", "reverse_sorted", "nearly_sorted", "duplicate_heavy")
KEYS = ("Student_ID", "CGPA", "Marks")
SIZES = (1000, 10000, 50000, 100000)

RESULT_FIELDS = [
    "timestamp_utc",
    "dataset_size",
    "condition",
    "dataset_file",
    "algorithm",
    "sorting_key",
    "run",
    "status",
    "execution_time_sec",
    "comparisons",
    "swaps",
    "moves",
    "peak_memory_mb",
    "verified",
    "timeout_sec",
    "error",
]


def parse_csv_list(value: str, allowed: tuple[str, ...], label: str) -> list[str]:
    values = [item.strip() for item in value.split(",") if item.strip()]
    invalid = [item for item in values if item not in allowed]
    if invalid:
        raise ValueError(f"Invalid {label}: {', '.join(invalid)}")
    return values


def parse_sizes(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    invalid = [value for value in values if value not in SIZES]
    if invalid:
        raise ValueError(f"Unsupported sizes: {invalid}. Allowed: {list(SIZES)}")
    return values


def dataset_path(root: Path, size: int, condition: str) -> Path:
    filename = f"students_{size}_{condition}.csv"
    return root / "data" / "generated" / condition / filename


def execute_worker(
    project_root: Path,
    dataset: Path,
    algorithm: str,
    key: str,
    timeout: float,
) -> dict:
    command = [
        sys.executable,
        "-m",
        "benchmark.worker",
        "--file",
        str(dataset),
        "--algorithm",
        algorithm,
        "--key",
        key,
    ]

    try:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "execution_time_sec": "",
            "comparisons": "",
            "swaps": "",
            "moves": "",
            "peak_memory_mb": "",
            "verified": False,
            "error": f"Exceeded timeout of {timeout:g} seconds",
        }

    stdout = completed.stdout.strip().splitlines()
    if stdout:
        try:
            result = json.loads(stdout[-1])
        except json.JSONDecodeError:
            result = None
    else:
        result = None

    if result is None:
        error = completed.stderr.strip() or "Worker returned no JSON result"
        return {
            "status": "ERROR",
            "execution_time_sec": "",
            "comparisons": "",
            "swaps": "",
            "moves": "",
            "peak_memory_mb": "",
            "verified": False,
            "error": error[-1000:],
        }

    if completed.returncode != 0 and result.get("status") == "COMPLETED":
        result["status"] = "ERROR"
        result["error"] = completed.stderr.strip()[-1000:]

    return result


def run_benchmarks(
    project_root: Path,
    sizes: list[int],
    conditions: list[str],
    keys: list[str],
    algorithms: list[str],
    repeats: int,
    timeout: float,
    output: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    total = len(sizes) * len(conditions) * len(keys) * len(algorithms) * repeats
    completed_count = 0

    print(f"Planned runs: {total}")
    print(f"Timeout per run: {timeout:g}s")

    for size in sizes:
        for condition in conditions:
            dataset = dataset_path(project_root, size, condition)
            if not dataset.exists():
                raise FileNotFoundError(f"Dataset not found: {dataset}")

            for key in keys:
                for algorithm in algorithms:
                    for run_number in range(1, repeats + 1):
                        completed_count += 1
                        print(
                            f"[{completed_count}/{total}] "
                            f"{algorithm:9s} | {key:10s} | {condition:15s} | {size:6d} | run {run_number}",
                            flush=True,
                        )
                        started = time.perf_counter()
                        result = execute_worker(
                            project_root, dataset, algorithm, key, timeout
                        )
                        launcher_elapsed = time.perf_counter() - started

                        row = {
                            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                            "dataset_size": size,
                            "condition": condition,
                            "dataset_file": str(dataset.relative_to(project_root)),
                            "algorithm": algorithm,
                            "sorting_key": key,
                            "run": run_number,
                            "status": result.get("status", "ERROR"),
                            "execution_time_sec": result.get("execution_time_sec", ""),
                            "comparisons": result.get("comparisons", ""),
                            "swaps": result.get("swaps", ""),
                            "moves": result.get("moves", ""),
                            "peak_memory_mb": result.get("peak_memory_mb", ""),
                            "verified": result.get("verified", False),
                            "timeout_sec": timeout,
                            "error": result.get("error", ""),
                        }
                        rows.append(row)

                        if row["status"] == "COMPLETED":
                            print(
                                f"    {float(row['execution_time_sec']):.6f}s | "
                                f"comparisons={row['comparisons']} | "
                                f"swaps={row['swaps']} | moves={row['moves']} | "
                                f"peak={float(row['peak_memory_mb']):.3f} MiB"
                            )
                        else:
                            print(
                                f"    {row['status']} | {row['error']} | "
                                f"launcher_elapsed={launcher_elapsed:.2f}s"
                            )

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    completed = sum(row["status"] == "COMPLETED" for row in rows)
    timed_out = sum(row["status"] == "TIMEOUT" for row in rows)
    errors = sum(row["status"] == "ERROR" for row in rows)
    print("\nBenchmark finished.")
    print(f"Completed: {completed} | Timeouts: {timed_out} | Errors: {errors}")
    print(f"Results: {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark all project sorting algorithms")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--sizes", default="1000,10000,50000,100000")
    parser.add_argument("--conditions", default=",".join(CONDITIONS))
    parser.add_argument("--keys", default=",".join(KEYS))
    parser.add_argument("--algorithms", default=",".join(ALGORITHMS))
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Maximum wall-clock time per algorithm/key/dataset run",
    )
    parser.add_argument(
        "--output",
        default="results/benchmark_results.csv",
        help="Output CSV path relative to project root",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than 0")

    project_root = Path(args.project_root).resolve()
    sizes = parse_sizes(args.sizes)
    conditions = parse_csv_list(args.conditions, CONDITIONS, "conditions")
    keys = parse_csv_list(args.keys, KEYS, "keys")
    algorithms = parse_csv_list(args.algorithms, ALGORITHMS, "algorithms")
    output = Path(args.output)
    if not output.is_absolute():
        output = project_root / output

    run_benchmarks(
        project_root,
        sizes,
        conditions,
        keys,
        algorithms,
        args.repeats,
        args.timeout,
        output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
