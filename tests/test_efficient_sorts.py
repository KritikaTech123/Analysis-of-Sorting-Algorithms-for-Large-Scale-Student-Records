import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from algorithms import merge_sort, quick_sort, sort_records_efficient


class EfficientSortTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"Student_ID": 100005, "Name": "E", "Department": "CSE", "Semester": 4, "CGPA": 7.2, "Attendance": 80.0, "Marks": 70},
            {"Student_ID": 100001, "Name": "A", "Department": "ECE", "Semester": 2, "CGPA": 9.1, "Attendance": 90.0, "Marks": 92},
            {"Student_ID": 100004, "Name": "D", "Department": "ME", "Semester": 6, "CGPA": 8.0, "Attendance": 75.0, "Marks": 85},
            {"Student_ID": 100002, "Name": "B", "Department": "CSE", "Semester": 3, "CGPA": 8.0, "Attendance": 88.0, "Marks": 65},
            {"Student_ID": 100003, "Name": "C", "Department": "CE", "Semester": 5, "CGPA": 6.5, "Attendance": 70.0, "Marks": 85},
        ]

    def assert_sorted(self, sort_fn):
        for key in ("Student_ID", "CGPA", "Marks"):
            records = list(self.records)
            expected = sorted(records, key=lambda r: r[key])
            metrics = sort_fn(records, key)
            self.assertEqual([r[key] for r in records], [r[key] for r in expected])
            self.assertGreaterEqual(metrics.comparisons, 0)
            self.assertGreaterEqual(metrics.swaps, 0)
            self.assertGreaterEqual(metrics.moves, 0)

    def test_merge_sort(self):
        self.assert_sorted(merge_sort)

    def test_quick_sort(self):
        self.assert_sorted(quick_sort)

    def test_dispatcher(self):
        for name, fn in (("merge", merge_sort), ("merge_sort", merge_sort),
                         ("quick", quick_sort), ("quick_sort", quick_sort)):
            records = list(self.records)
            expected_keys = sorted(r["Marks"] for r in records)
            sort_records_efficient(records, name, "Marks")
            self.assertEqual([r["Marks"] for r in records], expected_keys)

    def test_empty_and_single(self):
        for fn in (merge_sort, quick_sort):
            records = []
            metrics = fn(records)
            self.assertEqual(records, [])
            self.assertEqual(metrics.comparisons, 0)

            one = [dict(self.records[0])]
            metrics = fn(one)
            self.assertEqual(one, [self.records[0]])
            self.assertEqual(metrics.comparisons, 0)

    def test_duplicate_keys(self):
        records = [
            {"Student_ID": 3, "CGPA": 8.0, "Marks": 85},
            {"Student_ID": 1, "CGPA": 8.0, "Marks": 85},
            {"Student_ID": 2, "CGPA": 8.0, "Marks": 85},
            {"Student_ID": 4, "CGPA": 8.0, "Marks": 85},
        ]
        for fn in (merge_sort, quick_sort):
            data = list(records)
            fn(data, "CGPA")
            self.assertEqual([r["CGPA"] for r in data], [8.0] * 4)

    def test_invalid_key(self):
        for fn in (merge_sort, quick_sort):
            with self.assertRaises(ValueError):
                fn(list(self.records), "InvalidKey")

    def test_actual_member1_dataset_if_available(self):
        project_root = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(
            project_root, "data", "generated", "random", "students_1000_random.csv"
        )
        if not os.path.exists(path):
            self.skipTest("Member 1 dataset is not present in this checkout")

        with open(path, newline="", encoding="utf-8") as f:
            records = list(csv.DictReader(f))

        records = [
            {
                **r,
                "Student_ID": int(r["Student_ID"]),
                "CGPA": float(r["CGPA"]),
                "Marks": int(r["Marks"]),
            }
            for r in records
        ]

        for fn in (merge_sort, quick_sort):
            for key in ("Student_ID", "CGPA", "Marks"):
                data = list(records)
                fn(data, key)
                values = [r[key] for r in data]
                self.assertEqual(values, sorted(values))


if __name__ == "__main__":
    unittest.main()
