# Dataset — Student Records for Sorting Algorithm Comparison

## Purpose
Reproducible, validated student-record CSV datasets for comparing sorting algorithms across different input conditions and sizes.

## Columns
Student_ID (unique int), Name (string), Department (CSE/ECE/ME/CE/EEE), Semester (1-8), CGPA (0-10), Attendance (0-100), Marks (0-100)

## Dataset Sizes
1,000 / 10,000 / 50,000 / 100,000

## Input Conditions
Random, Sorted, Reverse Sorted, Nearly Sorted (~5% swapped), Duplicate Heavy (CGPA/Marks repeated, Student_ID unique)

## File Naming Convention
students_<size>_<condition>.csv under data/generated/<condition>/

## Reproducibility
Default random seed: 42

## Validation
All 20 files validated for row count, columns, uniqueness, missing values, ranges, ordering. Result: PASS.

## Sorting Keys Supported
Student_ID, CGPA, Marks