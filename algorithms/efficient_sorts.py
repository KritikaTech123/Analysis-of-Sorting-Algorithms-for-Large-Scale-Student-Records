"""Efficient sorting algorithms for the student-record sorting project.

Member 3 implementation:
- Merge Sort
- Quick Sort

Both algorithms sort a list of student-record dictionaries in place and
return the common ``SortMetrics`` object used by Member 2.  The supported
sorting keys are Student_ID, CGPA, and Marks.
"""

from typing import Any, Dict, List

from .basic_sorts import SUPPORTED_KEYS, SortMetrics, _key_function, _validate_records


Record = Dict[str, Any]


def merge_sort(records: List[Record], key: str = "Student_ID") -> SortMetrics:
    """Sort records in ascending order using Merge Sort.

    Complexity:
        Best:    O(n log n)
        Average: O(n log n)
        Worst:   O(n log n)
        Extra space: O(n)

    ``comparisons`` counts comparisons between record keys.
    ``moves`` counts record assignments into temporary/working arrays and
    back into the original list. ``swaps`` is zero because Merge Sort does
    not exchange elements in place.

    The input list is sorted in place.
    """
    _validate_records(records, key)
    metrics = SortMetrics()
    key_fn = _key_function(key)
    n = len(records)

    if n < 2:
        return metrics

    # One reusable buffer avoids allocating a new temporary list at every
    # recursive merge call.
    buffer: List[Record] = [records[0]] * n

    def merge(left: int, mid: int, right: int) -> None:
        i = left
        j = mid + 1
        k = left

        while i <= mid and j <= right:
            metrics.comparisons += 1
            if key_fn(records[i]) <= key_fn(records[j]):
                buffer[k] = records[i]
                metrics.moves += 1
                i += 1
            else:
                buffer[k] = records[j]
                metrics.moves += 1
                j += 1
            k += 1

        while i <= mid:
            buffer[k] = records[i]
            metrics.moves += 1
            i += 1
            k += 1

        while j <= right:
            buffer[k] = records[j]
            metrics.moves += 1
            j += 1
            k += 1

        for index in range(left, right + 1):
            records[index] = buffer[index]
            metrics.moves += 1

    def divide(left: int, right: int) -> None:
        if left >= right:
            return
        mid = left + (right - left) // 2
        divide(left, mid)
        divide(mid + 1, right)
        merge(left, mid, right)

    divide(0, n - 1)
    return metrics


def quick_sort(records: List[Record], key: str = "Student_ID") -> SortMetrics:
    """Sort records in ascending order using Quick Sort.

    A deterministic middle-element pivot is used.  The implementation uses
    Hoare partitioning and recurses on the smaller partition first, then
    continues with the larger partition.  This keeps the Python call stack
    bounded even when the input produces an unbalanced partition sequence.

    Complexity:
        Best:    O(n log n)
        Average: O(n log n)
        Worst:   O(n^2)
        Extra space: O(log n) average due to the controlled recursion stack;
                     O(log n) stack depth is maintained by recursing into the
                     smaller partition first.

    ``comparisons`` counts key comparisons performed during partitioning.
    ``swaps`` counts record exchanges and ``moves`` counts the three record
    assignments represented by each exchange.

    The input list is sorted in place.
    """
    _validate_records(records, key)
    metrics = SortMetrics()
    key_fn = _key_function(key)

    def swap(i: int, j: int) -> None:
        if i == j:
            return
        records[i], records[j] = records[j], records[i]
        metrics.swaps += 1
        metrics.moves += 3

    def partition(low: int, high: int) -> int:
        pivot = key_fn(records[low + (high - low) // 2])
        i = low - 1
        j = high + 1

        while True:
            # Move i right until a value >= pivot is found.
            while True:
                i += 1
                metrics.comparisons += 1
                if key_fn(records[i]) >= pivot:
                    break

            # Move j left until a value <= pivot is found.
            while True:
                j -= 1
                metrics.comparisons += 1
                if key_fn(records[j]) <= pivot:
                    break

            if i >= j:
                return j

            swap(i, j)

    def sort_range(low: int, high: int) -> None:
        # Recurse into the smaller partition and iterate over the larger one.
        # This prevents a worst-case recursion-depth failure on large inputs.
        while low < high:
            split = partition(low, high)

            left_size = split - low + 1
            right_size = high - split

            if left_size < right_size:
                sort_range(low, split)
                low = split + 1
            else:
                sort_range(split + 1, high)
                high = split

    if len(records) > 1:
        sort_range(0, len(records) - 1)

    return metrics


def sort_records_efficient(
    records: List[Record],
    algorithm: str,
    key: str = "Student_ID",
) -> SortMetrics:
    """Dispatch to Merge Sort or Quick Sort.

    Supported algorithm names are case-insensitive:
    ``merge``, ``merge_sort``, ``quick``, and ``quick_sort``.
    """
    normalized = algorithm.strip().lower().replace(" ", "_")
    algorithms = {
        "merge": merge_sort,
        "merge_sort": merge_sort,
        "quick": quick_sort,
        "quick_sort": quick_sort,
    }

    if normalized not in algorithms:
        supported = ", ".join(("merge", "quick"))
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Use: {supported}")

    return algorithms[normalized](records, key)
