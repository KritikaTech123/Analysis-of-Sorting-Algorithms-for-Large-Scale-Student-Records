import csv
import os
import random

FIELDNAMES = ["Student_ID", "Name", "Department", "Semester", "CGPA", "Attendance", "Marks"]
SIZES = [1000, 10000, 50000, 100000]
DEPARTMENTS = ["CSE", "ECE", "ME", "CE", "EEE"]

FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Kabir", "Sneha", "Vikram", "Isha", "Aditya", "Diya"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Kumar", "Reddy", "Jha", "Joshi", "Rao"]

SEED = 42


def generate_base_records(size, rng):
    """One deterministic base population per size — every condition below
    is derived from this SAME list, so all 5 CSVs for a size represent
    the same student population (required for fair sorting comparisons)."""
    records = []
    for i in range(size):
        student_id = 100001 + i
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        dept = rng.choice(DEPARTMENTS)
        semester = rng.randint(1, 8)
        cgpa = round(rng.uniform(0.0, 10.0), 2)
        attendance = round(rng.uniform(0.0, 100.0), 2)
        marks = rng.randint(0, 100)
        records.append({
            "Student_ID": student_id, "Name": name, "Department": dept,
            "Semester": semester, "CGPA": cgpa, "Attendance": attendance, "Marks": marks
        })
    return records


def to_random(records, rng):
    recs = records[:]
    rng.shuffle(recs)
    return recs


def to_sorted(records):
    return sorted(records, key=lambda r: r["Student_ID"])


def to_reverse_sorted(records):
    return sorted(records, key=lambda r: r["Student_ID"], reverse=True)


def to_nearly_sorted(records, rng, pct=0.05):
    """~5% of records are displaced from an otherwise sorted order.
    Uses rng.sample (no replacement) so the displaced fraction is accurate."""
    recs = to_sorted(records)
    n = len(recs)
    num_to_displace = int(n * pct)
    if num_to_displace % 2 == 1:
        num_to_displace -= 1
    if num_to_displace < 2:
        return recs
    indices = rng.sample(range(n), num_to_displace)
    for i in range(0, len(indices), 2):
        a, b = indices[i], indices[i + 1]
        recs[a], recs[b] = recs[b], recs[a]
    return recs


def to_duplicate_heavy(records, rng):
    """Student_ID stays unique. CGPA and Marks are redrawn from a small
    pool of values so those sorting keys contain many duplicates."""
    dup_cgpas = [6.0, 7.5, 8.0, 8.5, 9.0]
    dup_marks = [50, 65, 75, 85, 95]
    dup_records = []
    for r in records:
        r_copy = r.copy()
        r_copy["CGPA"] = rng.choice(dup_cgpas)
        r_copy["Marks"] = rng.choice(dup_marks)
        dup_records.append(r_copy)
    return dup_records


def save_to_csv(filepath, records):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def generate_all_datasets():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data", "generated")

    for size in SIZES:
        print(f"Generating datasets for size: {size}...")
        rng = random.Random(SEED)  # fresh, reproducible RNG per size

        base_records = generate_base_records(size, rng)

        random_records = to_random(base_records, rng)
        save_to_csv(os.path.join(base_dir, "random", f"students_{size}_random.csv"), random_records)

        sorted_records = to_sorted(base_records)
        save_to_csv(os.path.join(base_dir, "sorted", f"students_{size}_sorted.csv"), sorted_records)

        reverse_records = to_reverse_sorted(base_records)
        save_to_csv(os.path.join(base_dir, "reverse_sorted", f"students_{size}_reverse_sorted.csv"), reverse_records)

        nearly_records = to_nearly_sorted(base_records, rng, pct=0.05)
        save_to_csv(os.path.join(base_dir, "nearly_sorted", f"students_{size}_nearly_sorted.csv"), nearly_records)

        dup_records = to_duplicate_heavy(base_records, rng)
        save_to_csv(os.path.join(base_dir, "duplicate_heavy", f"students_{size}_duplicate_heavy.csv"), dup_records)

    print("All datasets generated successfully!")


if __name__ == "__main__":
    generate_all_datasets()