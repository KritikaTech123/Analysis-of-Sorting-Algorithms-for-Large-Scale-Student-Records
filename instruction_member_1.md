# Member 1 — Dataset & Data Generation
## Complete Implementation Instructions

### Project
**Design and Comparative Analysis of Sorting Algorithms for Large-Scale Student Records**

This document contains the complete task for **Member 1**. The goal is to finish the entire dataset/data-generation module before Members 2–5 begin their dependent work.

The project plan requires Member 1 to:
- design the student-record schema;
- generate datasets of different sizes;
- generate different input-order conditions;
- validate the generated data;
- provide a clean, documented dataset format that all sorting and benchmarking modules can use.

The project plan specifies dataset sizes of **1K, 10K, 50K, 100K, and optionally 500K/1M**, with input conditions **random, already sorted, reverse sorted, nearly sorted, and duplicate-heavy**. It also specifies sorting keys including **Student ID, CGPA, and Marks**. The exact requirements are from the supplied PBL plan. 

---

# 1. Your Final Responsibility

When you finish your work, the team should be able to take your generated files and immediately use them for:

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Merge Sort
5. Quick Sort
6. Benchmarking
7. Analysis and graphs
8. Final application/demo

**Do not implement the sorting algorithms.** Your job is to provide reliable, reproducible input data for them.

The most important rule is:

> All algorithms must receive equivalent datasets when comparisons are made.

This is necessary because the PBL specifically requires fair experiments using the same data and sorting key wherever possible.

---

# 2. Recommended Folder Structure

Create the following structure inside the project:

```text
project/
│
├── data/
│   ├── raw/
│   ├── generated/
│   │   ├── random/
│   │   ├── sorted/
│   │   ├── reverse_sorted/
│   │   ├── nearly_sorted/
│   │   └── duplicate_heavy/
│   │
│   └── README.md
│
├── generator/
│   ├── dataset_generator.*
│   ├── validator.*
│   └── README.md
│
└── ...
```

Replace `*` with the extension used by the team's selected programming language.

If the team has already selected a language/framework, follow that choice consistently. Do **not** introduce a second language just for the dataset module.

---

# 3. Student Record Schema

Use one consistent schema for every generated dataset.

Recommended CSV columns:

```text
Student_ID,Name,Department,Semester,CGPA,Attendance,Marks
```

### Field specification

| Field | Suggested Type | Example | Requirement |
|---|---|---|---|
| Student_ID | Integer | 100001 | Unique |
| Name | String | Aarav Sharma | Non-empty |
| Department | String | CSE | Valid department |
| Semester | Integer | 4 | Reasonable semester |
| CGPA | Decimal | 8.42 | 0–10 |
| Attendance | Decimal | 86.50 | 0–100 |
| Marks | Integer | 84 | 0–100 |

The PBL says student records **may contain** these fields. Use this schema consistently so the other members do not have to handle different formats.

---

# 4. Decide the Dataset Sizes

The required sizes are:

```text
1,000
10,000
50,000
100,000
```

Optionally add:

```text
500,000
1,000,000
```

Only generate 500K/1M if the machine can handle them comfortably.

### Minimum completion requirement

At minimum, you must successfully generate:

- 1K
- 10K
- 50K
- 100K

for all required input conditions.

If 500K/1M is feasible, generate them as well.

---

# 5. Generate the Base Dataset

First generate a **base/random dataset** for each size.

For example:

```text
data/generated/random/students_1000_random.csv
data/generated/random/students_10000_random.csv
data/generated/random/students_50000_random.csv
data/generated/random/students_100000_random.csv
```

The records should be valid student records.

### Important

Do not generate completely unrelated datasets for each sorting algorithm.

For example, if Member 2 tests Bubble Sort on:

```text
students_10000_random.csv
```

then Members 3 and 4 should be able to use the **same logical dataset** for Merge Sort and Quick Sort.

This is essential for fair comparison.

---

# 6. Generate the Five Required Input Conditions

For every dataset size, create the following five versions.

## A. Random

Records are in random order.

Example:

```text
Student_ID
100245
100011
100932
100101
...
```

This represents the normal/random input condition.

---

## B. Already Sorted

Sort records by the selected primary sorting key.

For consistency, use **Student_ID** as the default ordering key.

Example:

```text
100001
100002
100003
100004
...
```

The team can later sort the same data by CGPA or Marks for additional experiments.

---

## C. Reverse Sorted

Take the sorted dataset and reverse its order.

Example:

```text
100004
100003
100002
100001
```

This is particularly important for studying the behaviour of simple O(n²) algorithms.

---

## D. Nearly Sorted

Create a dataset that is mostly sorted but has a small percentage of records moved/swapped.

Recommended implementation:

1. Start with the sorted dataset.
2. Select approximately 5% of records.
3. Randomly swap their positions.
4. Keep the remaining 95% approximately in sorted order.

Example:

```text
100001
100002
100003
100812   <- displaced
100005
100006
...
```

Use the same rule for every dataset size.

Record the chosen percentage in the generator documentation.

---

## E. Duplicate-Heavy

Create data where the sorting key contains many duplicate values.

This does **not** mean duplicate student records.

Student IDs should remain unique.

Instead, create repeated values in fields such as:

- Marks
- CGPA
- Department
- Semester

For example, when testing the **Marks** key:

```text
85
72
85
85
91
72
85
72
...
```

The records themselves must still be different.

This condition is useful for studying how sorting algorithms behave when many comparison keys have equal values.

---

# 7. Recommended File Naming Convention

Use a predictable naming scheme:

```text
students_<size>_<condition>.csv
```

Examples:

```text
students_1000_random.csv
students_1000_sorted.csv
students_1000_reverse_sorted.csv
students_1000_nearly_sorted.csv
students_1000_duplicate_heavy.csv

students_10000_random.csv
students_10000_sorted.csv
students_10000_reverse_sorted.csv
students_10000_nearly_sorted.csv
students_10000_duplicate_heavy.csv
```

Continue the same pattern for:

```text
50000
100000
500000
1000000
```

Do not use inconsistent names such as:

```text
data1.csv
final.csv
final2.csv
newdata.csv
test.csv
```

The other members need predictable paths.

---

# 8. Reproducibility Requirement

The generator must use a fixed random seed by default.

For example:

```text
seed = 42
```

The exact seed value can be changed if the team agrees, but it must be documented.

Why?

If you generate the dataset today and regenerate it tomorrow, the same configuration should produce the same data.

The generator should ideally allow:

```text
size
condition
seed
output path
```

to be configured.

---

# 9. Generator Requirements

Your generator should support:

### Required

```text
generate random dataset
generate sorted dataset
generate reverse-sorted dataset
generate nearly-sorted dataset
generate duplicate-heavy dataset
```

### Recommended

Allow the user to specify:

```text
dataset size
random seed
output directory
```

For example, conceptually:

```text
generate_dataset(size=10000, condition="random", seed=42)
```

The exact function/command format depends on the team's language.

---

# 10. Validation Module

Do not stop after generating CSV files.

Create a validation program/script that checks the datasets.

At minimum, validate:

### 10.1 Row count

A 10K dataset must contain exactly:

```text
10,000 records
```

excluding the CSV header.

---

### 10.2 Required columns

Every file must contain:

```text
Student_ID
Name
Department
Semester
CGPA
Attendance
Marks
```

---

### 10.3 Student ID uniqueness

Check that:

```text
Student_ID
```

is unique.

There should not be two records with the same Student_ID.

---

### 10.4 Missing values

Check for:

```text
empty values
NULL
missing fields
```

The final datasets should not contain missing values.

---

### 10.5 Range validation

Check:

```text
Semester → valid semester range
CGPA → 0 to 10
Attendance → 0 to 100
Marks → 0 to 100
```

---

### 10.6 Sorted condition validation

For `sorted` datasets, verify that the selected key is ascending.

For `reverse_sorted`, verify descending order.

For `nearly_sorted`, verify that the dataset is mostly ordered and document the method used to create it.

For `duplicate_heavy`, verify that the chosen sorting key contains a high proportion of repeated values.

---

# 11. Cross-Dataset Consistency

This is one of your most important responsibilities.

For a particular size, the five conditions should be derived from the **same base records** whenever practical.

Example:

```text
students_10000_random.csv
students_10000_sorted.csv
students_10000_reverse_sorted.csv
students_10000_nearly_sorted.csv
students_10000_duplicate_heavy.csv
```

They should represent comparable student-record populations.

Do not make:

```text
random = students A
sorted = students B
reverse = students C
```

with unrelated records.

That would make the later performance comparison less meaningful.

---

# 12. Sorting Keys

The PBL requires experiments using at least 2–3 sorting keys.

The specified keys are:

```text
Student ID
CGPA
Marks
```

Your dataset must therefore contain all three.

You do **not** need to implement the sorting algorithms.

However, make sure the generated values make all three keys useful for testing.

### Important for duplicate-heavy testing

Student_ID should remain unique.

Use:

```text
CGPA
Marks
```

as the main duplicate-heavy keys.

---

# 13. Dataset README

Create:

```text
data/README.md
```

It should explain:

1. Dataset purpose
2. Column definitions
3. Dataset sizes
4. Input conditions
5. File naming convention
6. Random seed
7. How datasets were generated
8. How datasets were validated
9. Which files should be used for benchmarking

Example section:

```markdown
# Dataset

## Columns

- Student_ID
- Name
- Department
- Semester
- CGPA
- Attendance
- Marks

## Dataset Sizes

- 1,000
- 10,000
- 50,000
- 100,000

## Input Conditions

- Random
- Sorted
- Reverse Sorted
- Nearly Sorted
- Duplicate Heavy

## Reproducibility

Default random seed: 42
```

---

# 14. Generator README

Create:

```text
generator/README.md
```

Document:

- prerequisites;
- how to run the generator;
- how to select dataset size;
- how to select condition;
- how to generate all datasets;
- how to run validation;
- expected output locations.

Example:

```markdown
# Dataset Generator

## Generate all datasets

<command>

## Generate one dataset

<command>

## Validate datasets

<command>
```

Use the actual commands for the project's selected language.

---

# 15. Do Not Hard-Code Only One Dataset

Avoid writing a program that only does:

```text
generate 1000 records
```

The generator should be reusable.

It must support different sizes.

The other members will need datasets for:

```text
1K
10K
50K
100K
```

and potentially larger sizes.

---

# 16. Performance Considerations

Do not unnecessarily create extremely large objects in memory if the selected language allows streaming/file-based generation.

The project eventually deals with up to 500K/1M records.

The dataset generator should therefore be reasonably efficient.

However, **do not optimize at the cost of correctness**.

Correct and reproducible data is more important than premature optimization.

---

# 17. Final Checklist

Before telling the team that your work is complete, verify every item below.

## Code

- [ ] Dataset generator created
- [ ] Configurable dataset size
- [ ] Configurable random seed
- [ ] Random dataset generation
- [ ] Sorted dataset generation
- [ ] Reverse-sorted dataset generation
- [ ] Nearly-sorted dataset generation
- [ ] Duplicate-heavy dataset generation
- [ ] Validation program created
- [ ] No hard-coded single-size solution

## Data

- [ ] 1K datasets generated
- [ ] 10K datasets generated
- [ ] 50K datasets generated
- [ ] 100K datasets generated
- [ ] 500K generated if feasible
- [ ] 1M generated if feasible
- [ ] All required conditions generated
- [ ] Student IDs unique
- [ ] No missing values
- [ ] Values are within valid ranges
- [ ] Correct row counts
- [ ] Correct CSV headers

## Documentation

- [ ] `data/README.md`
- [ ] `generator/README.md`
- [ ] Column definitions documented
- [ ] Naming convention documented
- [ ] Random seed documented
- [ ] Nearly-sorted generation method documented
- [ ] Duplicate-heavy generation method documented
- [ ] Generation commands documented
- [ ] Validation commands documented

---

# 18. Final Handoff to Members 2–5

Do not simply send the message:

> "Dataset is done."

Instead, send the team a clear handoff.

Use this format:

```text
Member 1 Dataset Module — COMPLETED

Generated:
- 1K
- 10K
- 50K
- 100K
- [500K/1M if available]

Conditions:
- Random
- Sorted
- Reverse Sorted
- Nearly Sorted
- Duplicate Heavy

Sorting keys supported:
- Student_ID
- CGPA
- Marks

Dataset location:
data/generated/

Generator:
generator/dataset_generator.*

Validator:
generator/validator.*

Documentation:
data/README.md
generator/README.md

Default seed:
42

All datasets were validated for:
- row count
- required columns
- Student_ID uniqueness
- missing values
- valid ranges
- ordering conditions
```

---

# 19. Exact Handoff Contract for Other Members

The other members should be able to assume the following:

### Member 2 — Basic Sorting

Member 2 can directly load:

```text
data/generated/random/students_10000_random.csv
```

and implement Bubble, Selection, and Insertion Sort.

### Member 3 — Efficient Sorting

Member 3 can use the same dataset files for Merge Sort and Quick Sort.

### Member 4 — Benchmarking

Member 4 can systematically access:

```text
dataset size
+
input condition
+
sorting key
```

and run every algorithm under equivalent conditions.

### Member 5 — Integration

Member 5 can later use the generated datasets in the final interface.

---

# 20. What Counts as "DONE"

Your task is **not complete** merely because the generator runs once.

Member 1 is complete only when:

```text
Generator
    ↓
Generates all required dataset sizes
    ↓
Generates all five input conditions
    ↓
Produces consistent CSV files
    ↓
Validator checks every dataset
    ↓
README explains everything
    ↓
Other members can load the files without asking you
```

The final folder should be understandable to someone who did not write the generator.

---

# 21. Git Commit

When everything is tested, make a dedicated commit.

Suggested commit message:

```text
feat: add student dataset generator and validated datasets
```

If the repository uses multiple smaller commits, a reasonable sequence is:

```text
feat: add student record schema
feat: add dataset generator
feat: add input condition generators
feat: add dataset validator
docs: document dataset generation and validation
```

After pushing the completed work, inform the team that the dataset module is ready.

---

# 22. Important Rules

1. **Do not modify the sorting algorithms belonging to Members 2 and 3.**
2. **Do not create separate incompatible data formats.**
3. **Do not change column names without informing the team.**
4. **Do not remove Student_ID, CGPA, or Marks.**
5. **Do not use duplicate Student_ID values just to create duplicate-heavy data.**
6. **Do not compare algorithms using unrelated datasets.**
7. **Keep the random seed documented.**
8. **Validate before handing the data to the team.**
9. **Keep generated data out of source-code files.**
10. **Document every assumption you make.**

---

# 23. Definition of Success

At the end of Member 1's work, the repository should contain a **reproducible, validated, well-documented dataset-generation system**.

Members 2, 3, 4, and 5 should be able to start their work without needing to design the student schema, generate data, decide file naming, or clean broken datasets.

**Member 1's output is the foundation for the remaining project.**
