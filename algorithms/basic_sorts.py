"""Basic sorting algorithms for the student-record sorting project.

Implementation:
- Bubble Sort
- Selection Sort
- Insertion Sort

The algorithms operate on lists of student-record dictionaries and support
Student_ID, CGPA, and Marks as sorting keys. Each algorithm returns metrics
for comparisons, swaps, and moves so the benchmarking module can collect
results without modifying the sorting logic.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Sequence, Tuple


Record = Dict[str, Any]

SUPPORTED_KEYS = ("Student_ID", "CGPA", "Marks")


@dataclass
class SortMetrics:
    """Operation counters produced by a sorting algorithm.

    comparisons: number of key-to-key comparisons.
    swaps: number of element exchanges. Insertion Sort does not exchange
        elements, so its swap count is zero.
    moves: number of record assignments/movements performed by the algorithm.
        For an exchange, three assignments are counted.
    """

    comparisons: int = 0
    swaps: int = 0
    moves: int = 0

    def as_dict(self) -> Dict[str, int]:
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "moves": self.moves,
        }


def _key_function(key: str) -> Callable[[Record], Any]:
    """Return a key extractor after validating the requested sorting key."""
    if key not in SUPPORTED_KEYS:
        supported = ", ".join(SUPPORTED_KEYS)
        raise ValueError(f"Unsupported sorting key '{key}'. Use: {supported}")
    return lambda record: record[key]


def _validate_records(records: Sequence[Record], key: str) -> None:
    """Validate the input shape before sorting."""
    _key_function(key)
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise TypeError(f"Record at index {index} is not a dictionary")
        if key not in record:
            raise KeyError(f"Record at index {index} does not contain '{key}'")


def _swap(records: List[Record], i: int, j: int, metrics: SortMetrics) -> None:
    """Exchange two records and update swap/move counters."""
    records[i], records[j] = records[j], records[i]
    metrics.swaps += 1
    metrics.moves += 3


def bubble_sort(records: List[Record], key: str = "Student_ID") -> SortMetrics:
    """Sort records in ascending order using Bubble Sort.

    Complexity:
        Best:    O(n) with early termination
        Average: O(n^2)
        Worst:   O(n^2)
        Extra space: O(1)

    The input list is sorted in place.
    """
    _validate_records(records, key)
    metrics = SortMetrics()
    key_fn = _key_function(key)
    n = len(records)

    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(end):
            metrics.comparisons += 1
            if key_fn(records[j]) > key_fn(records[j + 1]):
                _swap(records, j, j + 1, metrics)
                swapped = True
        if not swapped:
            break

    return metrics


def selection_sort(records: List[Record], key: str = "Student_ID") -> SortMetrics:
    """Sort records in ascending order using Selection Sort.

    Complexity:
        Best:    O(n^2)
        Average: O(n^2)
        Worst:   O(n^2)
        Extra space: O(1)

    The input list is sorted in place.
    """
    _validate_records(records, key)
    metrics = SortMetrics()
    key_fn = _key_function(key)
    n = len(records)

    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            metrics.comparisons += 1
            if key_fn(records[j]) < key_fn(records[min_index]):
                min_index = j

        if min_index != i:
            _swap(records, i, min_index, metrics)

    return metrics


def insertion_sort(records: List[Record], key: str = "Student_ID") -> SortMetrics:
    """Sort records in ascending order using Insertion Sort.

    Complexity:
        Best:    O(n)
        Average: O(n^2)
        Worst:   O(n^2)
        Extra space: O(1)

    The input list is sorted in place. Insertion Sort shifts records instead
    of exchanging them, so ``swaps`` remains zero while ``moves`` counts
    record assignments caused by shifts and insertion.
    """
    _validate_records(records, key)
    metrics = SortMetrics()
    key_fn = _key_function(key)

    for i in range(1, len(records)):
        current = records[i]
        current_key = key_fn(current)
        j = i - 1

        while j >= 0:
            metrics.comparisons += 1
            if key_fn(records[j]) <= current_key:
                break
            records[j + 1] = records[j]
            metrics.moves += 1
            j -= 1

        records[j + 1] = current
        metrics.moves += 1

    return metrics


def sort_records(
    records: List[Record],
    algorithm: str,
    key: str = "Student_ID",
) -> SortMetrics:
    """Dispatch to one of Member 2's basic sorting algorithms.

    Supported algorithm names are case-insensitive:
    ``bubble``, ``selection``, and ``insertion``.
    """
    normalized = algorithm.strip().lower().replace(" ", "_")
    algorithms = {
        "bubble": bubble_sort,
        "bubble_sort": bubble_sort,
        "selection": selection_sort,
        "selection_sort": selection_sort,
        "insertion": insertion_sort,
        "insertion_sort": insertion_sort,
    }

    if normalized not in algorithms:
        supported = ", ".join(("bubble", "selection", "insertion"))
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Use: {supported}")

    return algorithms[normalized](records, key)
