# Benchmarking Module 

This module runs the five sorting algorithms under the same dataset, input condition, sorting key, and experimental settings, then stores structured results.

## Algorithms

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort

## Metrics

- Execution time — measured only around the sorting call; CSV loading is excluded.
- Comparisons
- Swaps
- Moves
- Peak auxiliary Python memory — measured with `tracemalloc` during sorting.

## Why a separate worker process?

Bubble, Selection, and Insertion Sort are O(n²). They can become impractical on large inputs. Each run therefore gets its own process and a configurable timeout. A timeout is recorded as `TIMEOUT`; it is never converted into a fake timing value.

## Basic command

From the project root:

```bash
python -m benchmark.run_benchmark
```

Default configuration tests every combination of:

- 1K, 10K, 50K, 100K
- random, sorted, reverse_sorted, nearly_sorted, duplicate_heavy
- Student_ID, CGPA, Marks
- all five algorithms
- one run per combination
- 10 second timeout per run

## Recommended first run

For a quick check:

```bash
python -m benchmark.run_benchmark --sizes 1000 --repeats 1 --timeout 30
```

## Custom run

```bash
python -m benchmark.run_benchmark \
  --sizes 1000,10000 \
  --conditions random,sorted,reverse_sorted \
  --keys Student_ID,CGPA,Marks \
  --algorithms bubble,selection,insertion,merge,quick \
  --repeats 2 \
  --timeout 30 \
  --output results/benchmark_results.csv
```

## Analysis

After benchmarking:

```bash
python -m analysis.analyze_results
```

This creates:

```text
results/benchmark_summary.csv
plots/*.png
```

## Fairness rule

The benchmark never sorts one algorithm's private/random copy generated independently from another algorithm. Every run loads the same named CSV dataset for the selected size and condition. The working list is a fresh copy inside that run, so one algorithm cannot modify the file or affect another run.

## Interpretation rule

Do not replace timeout rows with zero or estimated values. Large O(n²) algorithms may legitimately time out at large dataset sizes. The final report should explicitly distinguish measured results from theoretical complexity.
