import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

employees = pd.read_csv(DATA_DIR / "employees.csv")
performance = pd.read_csv(DATA_DIR / "performance.csv")
training = pd.read_csv(DATA_DIR / "training.csv")
absence = pd.read_csv(DATA_DIR / "absence.csv")

print("Missing values per dataset:\n")

print("Employees")
print(employees.isna().sum())

print("\nPerformance")
print(performance.isna().sum())

print("\nTraining")
print(training.isna().sum())

print("\nAbsence")
print(absence.isna().sum())
