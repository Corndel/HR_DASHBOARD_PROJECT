import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

employees = pd.read_csv(DATA_DIR / "employees.csv")
performance = pd.read_csv(DATA_DIR / "performance.csv")
training = pd.read_csv(DATA_DIR / "training.csv")
absence = pd.read_csv(DATA_DIR / "absence.csv")

print("EMPLOYEES")
print(employees.info())

print("\nPERFORMANCE")
print(performance.info())

print("\nTRAINING")
print(training.info())

print("\nABSENCE")
print(absence.info())
