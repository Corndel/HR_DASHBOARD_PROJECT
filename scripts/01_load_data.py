print("RUNNING FILE:", __file__)

import pandas as pd
from pathlib import Path

# Resolve project root
BASE_DIR = Path(__file__).resolve().parent.parent

print("BASE DIR:", BASE_DIR)
print("CONTENTS:", list(BASE_DIR.iterdir()))

DATA_DIR = BASE_DIR / "data"
print("DATA DIR:", DATA_DIR)
print("DATA CONTENTS:", list(DATA_DIR.iterdir()))

employees = pd.read_csv(DATA_DIR / "employees.csv")
performance = pd.read_csv(DATA_DIR / "performance.csv")
training = pd.read_csv(DATA_DIR / "training.csv")
absence = pd.read_csv(DATA_DIR / "absence.csv")

print("\nEmployees:")
print(employees.head())
