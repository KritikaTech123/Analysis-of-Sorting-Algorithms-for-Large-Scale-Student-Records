# Benchmarking & Data Analysis

## Responsibility

Run fair experiments on the five sorting algorithms and collect:

- execution time
- comparisons
- swaps
- moves
- peak auxiliary memory

The PBL plan requires experiments across dataset sizes, input conditions, and sorting keys, with results stored in a structured CSV and visualized.

## Files

```text
benchmark/
├── __init__.py
├── worker.py
├── run_benchmark.py
└── README.md

analysis/
├── __init__.py
├── analyze_results.py
└── README.md

tests/
└── test_benchmark.py

results/
└── .gitkeep

plots/
└── .gitkeep
```

## Quick verification

```bash
python -m unittest discover -s tests -v
```

## Quick benchmark

```bash
python -m benchmark.run_benchmark --sizes 1000 --timeout 30
```

## Full experiment

```bash
python -m benchmark.run_benchmark --repeats 1 --timeout 10
```

Then:

```bash
python -m analysis.analyze_results
```

## Important

A timeout is a real experimental result indicating that the selected algorithm did not finish within the configured practical limit. Never replace it with an invented execution time.
