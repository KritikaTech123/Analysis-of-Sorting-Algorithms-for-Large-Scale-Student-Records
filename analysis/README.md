# Analysis Module

`analyze_results.py` reads the structured benchmark CSV, keeps only completed and verified runs, creates an aggregate summary, and generates graphs for:

- Execution Time vs Dataset Size
- Comparisons vs Dataset Size
- Swaps vs Dataset Size
- Moves vs Dataset Size
- Peak Auxiliary Memory vs Dataset Size

Graphs are separated by sorting key and input condition so unrelated experiments are not mixed together.
