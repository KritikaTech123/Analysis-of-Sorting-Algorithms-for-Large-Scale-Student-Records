"""Create summary tables and the five project-level benchmark graphs."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


def to_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: str):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def read_completed(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    completed = []
    for row in rows:
        if row.get("status") != "COMPLETED" or row.get("verified") != "True":
            continue
        parsed = dict(row)
        for field in ("execution_time_sec", "peak_memory_mb"):
            parsed[field] = to_float(row[field])
        for field in ("dataset_size", "run", "comparisons", "swaps", "moves"):
            parsed[field] = to_int(row[field])
        completed.append(parsed)
    return completed


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def write_summary(rows: list[dict], output: Path) -> None:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["dataset_size"], row["condition"], row["sorting_key"], row["algorithm"])].append(row)

    fields = [
        "dataset_size", "condition", "sorting_key", "algorithm", "runs",
        "mean_time_sec", "std_time_sec", "mean_comparisons", "mean_swaps",
        "mean_moves", "mean_peak_memory_mb",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for group_key in sorted(groups):
            group = groups[group_key]
            writer.writerow({
                "dataset_size": group_key[0],
                "condition": group_key[1],
                "sorting_key": group_key[2],
                "algorithm": group_key[3],
                "runs": len(group),
                "mean_time_sec": f"{mean([r['execution_time_sec'] for r in group]):.9f}",
                "std_time_sec": f"{stddev([r['execution_time_sec'] for r in group]):.9f}",
                "mean_comparisons": f"{mean([r['comparisons'] for r in group]):.3f}",
                "mean_swaps": f"{mean([r['swaps'] for r in group]):.3f}",
                "mean_moves": f"{mean([r['moves'] for r in group]):.3f}",
                "mean_peak_memory_mb": f"{mean([r['peak_memory_mb'] for r in group]):.6f}",
            })


def _group_metric(rows, metric, key, condition):
    grouped = defaultdict(list)
    for row in rows:
        if row["sorting_key"] == key and row["condition"] == condition:
            grouped[(row["algorithm"], row["dataset_size"])].append(row[metric])
    return grouped


def make_plots(rows: list[dict], output_dir: Path, key: str, condition: str, condition_size: int) -> None:
    """Generate exactly five concise figures matching the PBL visualization plan."""
    import matplotlib.pyplot as plt

    output_dir.mkdir(parents=True, exist_ok=True)
    algorithms = ("bubble", "selection", "insertion", "merge", "quick")

    # 1. Execution Time vs Dataset Size
    grouped = _group_metric(rows, "execution_time_sec", key, condition)
    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        points = sorted((size, mean(values)) for (alg, size), values in grouped.items() if alg == algorithm)
        if points:
            plt.plot([p[0] for p in points], [p[1] for p in points], marker="o", label=algorithm.title())
    plt.xlabel("Dataset Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Execution Time vs Dataset Size ({key}, {condition})")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "01_execution_time_vs_dataset_size.png", dpi=150)
    plt.close()

    # 2. Comparisons vs Dataset Size
    grouped = _group_metric(rows, "comparisons", key, condition)
    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        points = sorted((size, mean(values)) for (alg, size), values in grouped.items() if alg == algorithm)
        if points:
            plt.plot([p[0] for p in points], [p[1] for p in points], marker="o", label=algorithm.title())
    plt.xlabel("Dataset Size")
    plt.ylabel("Number of Comparisons")
    plt.title(f"Comparisons vs Dataset Size ({key}, {condition})")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "02_comparisons_vs_dataset_size.png", dpi=150)
    plt.close()

    # 3. Swaps/Moves vs Dataset Size — both metrics are shown because
    # insertion/merge naturally use moves instead of swaps.
    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        swap_group = _group_metric(rows, "swaps", key, condition)
        move_group = _group_metric(rows, "moves", key, condition)
        swap_points = sorted((size, mean(values)) for (alg, size), values in swap_group.items() if alg == algorithm)
        move_points = sorted((size, mean(values)) for (alg, size), values in move_group.items() if alg == algorithm)
        if swap_points:
            plt.plot([p[0] for p in swap_points], [p[1] for p in swap_points], marker="o", label=f"{algorithm.title()} swaps")
        if move_points:
            plt.plot([p[0] for p in move_points], [p[1] for p in move_points], marker="x", linestyle="--", label=f"{algorithm.title()} moves")
    plt.xlabel("Dataset Size")
    plt.ylabel("Count")
    plt.title(f"Swaps / Moves vs Dataset Size ({key}, {condition})")
    plt.legend(fontsize=8, ncol=2)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "03_swaps_moves_vs_dataset_size.png", dpi=150)
    plt.close()

    # 4. Random vs Sorted vs Reverse-Sorted — fixed size, same key.
    plt.figure(figsize=(10, 6))
    comparison_conditions = ("random", "sorted", "reverse_sorted")
    for algorithm in algorithms:
        values = []
        labels = []
        for cond in comparison_conditions:
            candidates = [r["execution_time_sec"] for r in rows
                          if r["sorting_key"] == key and r["condition"] == cond
                          and r["dataset_size"] == condition_size and r["algorithm"] == algorithm]
            if candidates:
                labels.append(cond.replace("_", " ").title())
                values.append(mean(candidates))
        if values:
            # Use one x-position per condition and connect the three measurements.
            plt.plot(range(len(values)), values, marker="o", label=algorithm.title())
    plt.xticks(range(3), [c.replace("_", " ").title() for c in comparison_conditions])
    plt.xlabel("Input Condition")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Input Order Effect at {condition_size:,} Records ({key})")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "04_random_sorted_reverse_comparison.png", dpi=150)
    plt.close()

    # 5. Memory Usage Comparison
    grouped = _group_metric(rows, "peak_memory_mb", key, condition)
    plt.figure(figsize=(9, 6))
    for algorithm in algorithms:
        points = sorted((size, mean(values)) for (alg, size), values in grouped.items() if alg == algorithm)
        if points:
            plt.plot([p[0] for p in points], [p[1] for p in points], marker="o", label=algorithm.title())
    plt.xlabel("Dataset Size")
    plt.ylabel("Peak Auxiliary Memory (MiB)")
    plt.title(f"Memory Usage vs Dataset Size ({key}, {condition})")
    plt.legend()
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(output_dir / "05_memory_usage_comparison.png", dpi=150)
    plt.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/benchmark_results.csv")
    parser.add_argument("--summary", default="results/benchmark_summary.csv")
    parser.add_argument("--plots", default="plots")
    parser.add_argument("--key", default="Student_ID", choices=("Student_ID", "CGPA", "Marks"))
    parser.add_argument("--condition", default="random", choices=("random", "sorted", "reverse_sorted", "nearly_sorted", "duplicate_heavy"))
    parser.add_argument("--condition-size", type=int, default=10000)
    parser.add_argument("--no-plots", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    rows = read_completed(Path(args.input))
    if not rows:
        raise SystemExit("No completed and verified benchmark rows found.")

    write_summary(rows, Path(args.summary))
    if not args.no_plots:
        make_plots(rows, Path(args.plots), args.key, args.condition, args.condition_size)

    print(f"Completed verified rows analysed: {len(rows)}")
    print(f"Summary: {args.summary}")
    if not args.no_plots:
        print(f"Five project graphs: {args.plots}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
