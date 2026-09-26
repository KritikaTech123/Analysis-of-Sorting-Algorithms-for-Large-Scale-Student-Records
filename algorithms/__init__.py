"""Sorting algorithms used by the project."""

from .basic_sorts import (
    SUPPORTED_KEYS,
    SortMetrics,
    bubble_sort,
    insertion_sort,
    selection_sort,
    sort_records,
)

__all__ = [
    "SUPPORTED_KEYS",
    "SortMetrics",
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "sort_records",
]
