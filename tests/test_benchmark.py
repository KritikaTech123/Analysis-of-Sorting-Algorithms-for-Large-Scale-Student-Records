import csv
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.worker import load_records, verify_sorted
from benchmark.run_benchmark import dataset_path, parse_csv_list, parse_sizes


class BenchmarkTests(unittest.TestCase):
    def test_parse_sizes(self):
        self.assertEqual(parse_sizes("1000,10000"), [1000, 10000])
        with self.assertRaises(ValueError):
            parse_sizes("123")

    def test_parse_csv_list(self):
        self.assertEqual(parse_csv_list("random,sorted", ("random", "sorted"), "conditions"), ["random", "sorted"])
        with self.assertRaises(ValueError):
            parse_csv_list("random,bad", ("random", "sorted"), "conditions")

    def test_dataset_path(self):
        root = Path("project")
        self.assertEqual(
            dataset_path(root, 1000, "random"),
            root / "data" / "generated" / "random" / "students_1000_random.csv",
        )

    def test_load_and_verify_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.csv"
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Student_ID", "Name", "Department", "Semester", "CGPA", "Attendance", "Marks"])
                writer.writerow([100002, "B", "CSE", 2, 8.0, 80.0, 70])
                writer.writerow([100001, "A", "ECE", 2, 9.0, 90.0, 90])

            records = load_records(path)
            self.assertEqual(records[0]["Student_ID"], 100002)
            self.assertFalse(verify_sorted(records, "Student_ID"))
            records.sort(key=lambda r: r["Student_ID"])
            self.assertTrue(verify_sorted(records, "Student_ID"))


if __name__ == "__main__":
    unittest.main()
