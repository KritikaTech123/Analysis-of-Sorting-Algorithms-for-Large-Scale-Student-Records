# Analytics Handoff

## Completed responsibility

Benchmarking and Data Analysis for the sorting-algorithm PBL.

## Added

- `benchmark/worker.py` — executes one algorithm/key experiment and records time, comparisons, swaps, moves, and peak auxiliary memory.
- `benchmark/run_benchmark.py` — runs the experiment matrix and writes `results/benchmark_results.csv`.
- `analysis/analyze_results.py` — aggregates completed verified results and creates the five required project-level graphs.
- `tests/test_benchmark.py` — tests benchmark utilities.
- Documentation and `requirements.txt`.

## Handoff contract

Member 4 expects Member 1's datasets at:

```text
data/generated/<condition>/students_<size>_<condition>.csv
```

and Member 2/3's algorithms exposed through:

```python
from algorithms import bubble_sort, selection_sort, insertion_sort
from algorithms import merge_sort, quick_sort
```

## Commands

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m benchmark.run_benchmark
python -m analysis.analyze_results
```

For a quick test:

```bash
python -m benchmark.run_benchmark --sizes 1000 --algorithms merge,quick --timeout 30 --output results/smoke_results.csv
python -m analysis.analyze_results --input results/smoke_results.csv --summary results/smoke_summary.csv --plots plots/smoke --condition-size 1000
```

Do not commit generated benchmark CSVs or PNGs unless the team specifically wants to preserve a particular experiment run. The code and reproducible commands are the primary deliverable.
