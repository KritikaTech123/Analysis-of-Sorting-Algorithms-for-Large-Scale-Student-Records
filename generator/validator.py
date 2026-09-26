import csv
import os
import re
import sys

REQUIRED_COLUMNS = ["Student_ID", "Name", "Department", "Semester", "CGPA", "Attendance", "Marks"]
RANGES = {"Semester": (1, 8), "CGPA": (0.0, 10.0), "Attendance": (0.0, 100.0), "Marks": (0, 100)}
FILENAME_RE = re.compile(r"students_(\d+)_(random|sorted|reverse_sorted|nearly_sorted|duplicate_heavy)\.csv$")
NEARLY_SORTED_TOLERANCE = 0.10
DUPLICATE_HEAVY_MIN_REPEAT_RATIO = 0.5


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def validate_file(path):
    filename = os.path.basename(path)
    m = FILENAME_RE.search(filename)
    errors = []
    if not m:
        return [f"Filename doesn't match convention: {filename}"]

    expected_size, condition = int(m.group(1)), m.group(2)
    header, rows = load_rows(path)

    if header != REQUIRED_COLUMNS:
        errors.append(f"Column mismatch: {header}")
    if len(rows) != expected_size:
        errors.append(f"Row count {len(rows)} != expected {expected_size}")

    ids = [r.get("Student_ID", "") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("Student_ID not unique")

    integer_ids = []
    for value in ids:
        try:
            integer_ids.append(int(value))
        except (ValueError, TypeError):
            errors.append(f"Student_ID is not an integer: {value!r}")

    for r in rows:
        for col in REQUIRED_COLUMNS:
            if not str(r.get(col, "")).strip():
                errors.append(f"Missing value in {col}")
                break

    for r in rows:
        try:
            checks = [
                (int(r["Semester"]), RANGES["Semester"]),
                (float(r["CGPA"]), RANGES["CGPA"]),
                (float(r["Attendance"]), RANGES["Attendance"]),
                (int(r["Marks"]), RANGES["Marks"]),
            ]
            for val, (lo, hi) in checks:
                if not (lo <= val <= hi):
                    errors.append(f"Out-of-range value: {val}")
        except (ValueError, TypeError):
            errors.append("Malformed numeric field")

    if condition == "sorted":
        vals = [int(r["Student_ID"]) for r in rows]
        if vals != sorted(vals):
            errors.append("'sorted' file is not ascending")
    elif condition == "reverse_sorted":
        vals = [int(r["Student_ID"]) for r in rows]
        if vals != sorted(vals, reverse=True):
            errors.append("'reverse_sorted' file is not descending")
    elif condition == "nearly_sorted":
        vals = [int(r["Student_ID"]) for r in rows]
        sv = sorted(vals)
        disp = sum(1 for a, b in zip(vals, sv) if a != b)
        ratio = disp / len(vals) if vals else 0
        if ratio > NEARLY_SORTED_TOLERANCE:
            errors.append(f"nearly_sorted displaced {ratio:.1%}, exceeds {NEARLY_SORTED_TOLERANCE:.0%} tolerance")

    if condition == "duplicate_heavy":
        for key in ("CGPA", "Marks"):
            vals = [r[key] for r in rows]
            repeat_ratio = 1 - (len(set(vals)) / len(vals)) if vals else 0
            if repeat_ratio < DUPLICATE_HEAVY_MIN_REPEAT_RATIO:
                errors.append(f"duplicate_heavy: {key} repeat ratio {repeat_ratio:.1%} too low")

    return errors


def find_csv_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".csv"):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "data", "generated")
    targets = find_csv_files(root)
    if not targets:
        print("No CSV files found.")
        sys.exit(1)

    all_ok = True
    for path in targets:
        errors = validate_file(path)
        status = "PASS" if not errors else "FAIL"
        if errors:
            all_ok = False
        print(f"[{status}] {path}")
        for e in errors:
            print(f"    - {e}")

    print()
    print("All datasets valid." if all_ok else "Validation FAILED.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()