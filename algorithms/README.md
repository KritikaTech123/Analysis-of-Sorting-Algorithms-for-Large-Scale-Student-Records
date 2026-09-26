# Sorting Algorithms

This module contains the sorting implementations for the project.

## Basic Sorting

- Bubble Sort
- Selection Sort
- Insertion Sort

File: `basic_sorts.py`

## Efficient Sorting

- Merge Sort
- Quick Sort

File: `efficient_sorts.py`

Both implementations use the same:

- record format: dictionary-based student records;
- sorting keys: `Student_ID`, `CGPA`, `Marks`;
- `SortMetrics` counters: comparisons, swaps, moves;
- in-place output convention: the supplied list is sorted and metrics are returned.

## Usage

```python
from algorithms import merge_sort, quick_sort

records = [
    {"Student_ID": 100003, "CGPA": 7.4, "Marks": 68},
    {"Student_ID": 100001, "CGPA": 9.1, "Marks": 92},
    {"Student_ID": 100002, "CGPA": 8.3, "Marks": 81},
]

metrics = merge_sort(records, key="CGPA")
print(records)
print(metrics.as_dict())

metrics = quick_sort(records, key="Marks")
print(records)
print(metrics.as_dict())
```

## Complexity

| Algorithm | Best | Average | Worst | Extra Space |
|---|---:|---:|---:|---:|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) stack with controlled recursion |

Quick Sort uses a deterministic middle-element pivot and Hoare partitioning. It recurses into the smaller partition first so large datasets do not cause Python recursion-depth failures.
