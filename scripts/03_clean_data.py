import pandas as pd
from pathlib import Path

# Define base and data directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load raw CSV files into DataFrames
employees = pd.read_csv(DATA_DIR / "employees.csv")
training = pd.read_csv(DATA_DIR / "training.csv")
absence = pd.read_csv(DATA_DIR / "absence.csv")

# Convert relevant columns to datetime format, handling errors gracefully
employees['join_date'] = pd.to_datetime(employees['join_date'], errors='coerce')
training['completion_date'] = pd.to_datetime(training['completion_date'], errors='coerce')
absence['absence_date'] = pd.to_datetime(absence['absence_date'], errors='coerce')

# Display data types to verify datetime conversion
print("Employees Data Types:\n", employees.dtypes)
print("\nTraining Data Types:\n", training.dtypes)
print("\nAbsence Data Types:\n", absence.dtypes)

# Show sample date values for quick validation
print("\nSample Employees Join Dates:\n", employees[['employee_id', 'join_date']].head())
print("\nSample Training Completion Dates:\n", training[['training_id', 'completion_date']].head())
print("\nSample Absence Dates:\n", absence[['absence_id', 'absence_date']].head())

# Identify missing values before any data imputation
print("\nMissing Values Before Handling:")
print("Employees:\n", employees.isna().sum())
print("\nTraining:\n", training.isna().sum())
print("\nAbsence:\n", absence.isna().sum())

# Fill missing 'employment_status' with 'Unknown' to avoid nulls
employees['employment_status'] = employees['employment_status'].fillna('Unknown')

# For training, keep missing 'completion_date' as NaT if 'completion_status' is 'Not Completed'
# No fill required here as missing dates represent incompletion

# Fill missing 'satisfaction_score' in absence with the mean score to minimize bias
absence['satisfaction_score'] = absence['satisfaction_score'].fillna(absence['satisfaction_score'].mean())

# Confirm missing values after handling
print("\nMissing Values After Handling:")
print("Employees:\n", employees.isna().sum())
print("\nTraining:\n", training.isna().sum())
print("\nAbsence:\n", absence.isna().sum())

# Inspect satisfaction score distribution and cap any values exceeding maximum expected score (10)
print("\nSatisfaction Score Summary Before Capping:")
print(absence['satisfaction_score'].describe())

absence.loc[absence['satisfaction_score'] > 10, 'satisfaction_score'] = 10

print("\nSatisfaction Score Summary After Capping:")
print(absence['satisfaction_score'].describe())

# Normalize categorical columns for consistency
employees['employment_status'] = employees['employment_status'].str.strip().str.capitalize()
training['mandatory'] = training['mandatory'].str.strip().str.capitalize()
training['completion_status'] = training['completion_status'].str.strip().str.capitalize()
absence['absence_type'] = absence['absence_type'].str.strip().str.capitalize()

# Display sample unique values after normalization to verify standardization
print("\nNormalized Employment Status Values:", employees['employment_status'].unique())
print("Normalized Training Mandatory Values:", training['mandatory'].unique())
print("Normalized Training Completion Status Values:", training['completion_status'].unique())
print("Normalized Absence Type Values:", absence['absence_type'].unique())

# Detect and report duplicate records in datasets to ensure data integrity
duplicate_employees = employees[employees.duplicated(subset=['employee_id'], keep=False)]
print("\nDuplicate Employee Records:\n", duplicate_employees)

duplicate_training = training[training.duplicated(subset=['training_id'], keep=False)]
print("\nDuplicate Training Records:\n", duplicate_training)

duplicate_absence = absence[absence.duplicated(subset=['absence_id'], keep=False)]
print("\nDuplicate Absence Records:\n", duplicate_absence)

# Save cleaned data to new CSV files for downstream analysis and dashboard use
CLEAN_DATA_DIR = BASE_DIR / "clean_data"
CLEAN_DATA_DIR.mkdir(exist_ok=True)

employees.to_csv(CLEAN_DATA_DIR / "employees_clean.csv", index=False)
training.to_csv(CLEAN_DATA_DIR / "training_clean.csv", index=False)
absence.to_csv(CLEAN_DATA_DIR / "absence_clean.csv", index=False)

print("\nCleaned datasets have been saved to the 'clean_data' directory.")
