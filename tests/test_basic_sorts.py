import csv
import copy
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms.basic_sorts import (  # noqa: E402
    bubble_sort,
    insertion_sort,
    selection_sort,
    sort_records,
)


SAMPLE = [
    {"Student_ID": 100004, "CGPA": 8.20, "Marks": 72},
    {"Student_ID": 100001, "CGPA": 9.10, "Marks": 91},
    {"Student_ID": 100003, "CGPA": 6.70, "Marks": 65},
    {"Student_ID": 100002, "CGPA": 8.20, "Marks": 85},
]


def expected(records, key):
    return sorted(records, key=lambda row: row[key])


class TestBasicSorts(unittest.TestCase):
    def test_bubble_sort_all_keys(self):
        for key in ("Student_ID", "CGPA", "Marks"):
            records = copy.deepcopy(SAMPLE)
            metrics = bubble_sort(records, key)
            self.assertEqual(records, expected(SAMPLE, key))
            self.assertGreater(metrics.comparisons, 0)
            self.assertGreaterEqual(metrics.swaps, 0)

    def test_selection_sort_all_keys(self):
        for key in ("Student_ID", "CGPA", "Marks"):
            records = copy.deepcopy(SAMPLE)
            metrics = selection_sort(records, key)
            self.assertEqual(records, expected(SAMPLE, key))
            self.assertEqual(metrics.comparisons, len(SAMPLE) * (len(SAMPLE) - 1) // 2)
            self.assertGreaterEqual(metrics.swaps, 0)

    def test_insertion_sort_all_keys(self):
        for key in ("Student_ID", "CGPA", "Marks"):
            records = copy.deepcopy(SAMPLE)
            metrics = insertion_sort(records, key)
            self.assertEqual(records, expected(SAMPLE, key))
            self.assertGreater(metrics.comparisons, 0)
            self.assertEqual(metrics.swaps, 0)
            self.assertGreater(metrics.moves, 0)

    def test_dispatcher(self):
        for algorithm in (
            "bubble", "selection", "insertion",
            "bubble_sort", "selection_sort", "insertion_sort",
        ):
            records = copy.deepcopy(SAMPLE)
            sort_records(records, algorithm, "Marks")
            self.assertEqual(records, expected(SAMPLE, "Marks"))

    def test_empty_and_single_record_inputs(self):
        for algorithm in (bubble_sort, selection_sort, insertion_sort):
            records = []
            metrics = algorithm(records, "Student_ID")
            self.assertEqual(records, [])
            self.assertEqual(
                metrics.as_dict(),
                {"comparisons": 0, "swaps": 0, "moves": 0},
            )

            records = [copy.deepcopy(SAMPLE[0])]
            metrics = algorithm(records, "Student_ID")
            self.assertEqual(records, [SAMPLE[0]])
            self.assertEqual(
                metrics.as_dict(),
                {"comparisons": 0, "swaps": 0, "moves": 0},
            )

    def test_invalid_key(self):
        records = copy.deepcopy(SAMPLE)
        with self.assertRaises(ValueError):
            bubble_sort(records, "Name")

    def test_real_member1_dataset(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "data" / "generated" / "random" / "students_1000_random.csv"
        )
        if not path.exists():
            self.skipTest("Member 1 dataset is not present")

        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        records = []
        for row in rows[:100]:
            records.append(
                {
                    "Student_ID": int(row["Student_ID"]),
                    "Name": row["Name"],
                    "Department": row["Department"],
                    "Semester": int(row["Semester"]),
                    "CGPA": float(row["CGPA"]),
                    "Attendance": float(row["Attendance"]),
                    "Marks": int(row["Marks"]),
                }
            )

        for algorithm in (bubble_sort, selection_sort, insertion_sort):
            for key in ("Student_ID", "CGPA", "Marks"):
                working = copy.deepcopy(records)
                algorithm(working, key)
                self.assertEqual(
                    [r[key] for r in working],
                    sorted(r[key] for r in records),
                )


if __name__ == "__main__":
    unittest.main()
