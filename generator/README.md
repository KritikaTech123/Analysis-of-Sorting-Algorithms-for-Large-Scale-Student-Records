# Dataset Generator — Member 1

## Prerequisites
Python 3.8+ (standard library only)

## Generate all datasets
python dataset_generator.py

## Validate datasets
python validator.py

## Expected output locations
data/generated/<condition>/students_<size>_<condition>.csv

## Reproducibility
Random seed fixed at 42 inside dataset_generator.pyGet-ChildItem -Recurse ..\data
