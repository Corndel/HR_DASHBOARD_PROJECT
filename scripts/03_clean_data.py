import pandas as pd
from pathlib import Path

# Get project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load your CSV files
employees = pd.read_csv(DATA_DIR / "employees.csv")
training = pd.read_csv(DATA_DIR / "training.csv")
absence = pd.read_csv(DATA_DIR / "absence.csv")

# Convert date columns to datetime format, fixing inconsistencies
employees['join_date'] = pd.to_datetime(employees['join_date'], errors='coerce')
training['completion_date'] = pd.to_datetime(training['completion_date'], errors='coerce')
absence['absence_date'] = pd.to_datetime(absence['absence_date'], errors='coerce')

# Print data types to check if dates converted properly
print("Employees Data Types:\n", employees.dtypes)
print("\nTraining Data Types:\n", training.dtypes)
print("\nAbsence Data Types:\n", absence.dtypes)

# Print first 5 rows of date columns to see sample
print("\nEmployees Join Dates:\n", employees[['employee_id', 'join_date']].head())
print("\nTraining Completion Dates:\n", training[['training_id', 'completion_date']].head())
print("\nAbsence Dates:\n", absence[['absence_id', 'absence_date']].head())

print("\nMissing values before handling:")

print("Employees missing values:\n", employees.isna().sum())
print("\nTraining missing values:\n", training.isna().sum())
print("\nAbsence missing values:\n", absence.isna().sum())

# Handle missing employment_status in employees by filling with 'Unknown'
employees['employment_status'] = employees['employment_status'].fillna('Unknown')

# For training completion_date missing (where completion_status = Not Completed), fill with a placeholder date or keep as NaT
# Here we keep NaT because no completion date means not done.

# If you want, you can fill satisfaction_score missing values in absence with the average or a default like 5
absence['satisfaction_score'] = absence['satisfaction_score'].fillna(absence['satisfaction_score'].mean())

print("\nMissing values after handling:")

print("Employees missing values:\n", employees.isna().sum())
print("\nTraining missing values:\n", training.isna().sum())
print("\nAbsence missing values:\n", absence.isna().sum())

print("\nChecking for outliers and invalid values:")

# Check satisfaction_score values range
print("Satisfaction Score range before correction:")
print(absence['satisfaction_score'].describe())

# Cap satisfaction_score at 10
absence.loc[absence['satisfaction_score'] > 10, 'satisfaction_score'] = 10

print("\nSatisfaction Score range after capping at 10:")
print(absence['satisfaction_score'].describe())

# (Optional) You can add other checks here, like negative days_absent, etc.

print("\nNormalizing categorical columns...")

# Normalize 'employment_status' in employees to lowercase, then capitalize (e.g., 'active', 'Active')
employees['employment_status'] = employees['employment_status'].str.strip().str.capitalize()

# Normalize 'mandatory' in training to consistent Yes/No
training['mandatory'] = training['mandatory'].str.strip().str.capitalize()

# Normalize 'completion_status' in training similarly
training['completion_status'] = training['completion_status'].str.strip().str.capitalize()

# Normalize 'absence_type' in absence
absence['absence_type'] = absence['absence_type'].str.strip().str.capitalize()

print("Sample normalized employment_status values:", employees['employment_status'].unique())
print("Sample normalized mandatory values:", training['mandatory'].unique())
print("Sample normalized completion_status values:", training['completion_status'].unique())
print("Sample normalized absence_type values:", absence['absence_type'].unique())



print("\nChecking for duplicates in datasets...")

# Check for duplicate employee IDs in employees dataset
duplicate_employees = employees[employees.duplicated(subset=['employee_id'], keep=False)]
print("Duplicate employee IDs:\n", duplicate_employees)

# Check for duplicate training IDs
duplicate_training = training[training.duplicated(subset=['training_id'], keep=False)]
print("Duplicate training IDs:\n", duplicate_training)

# Check for duplicate absence IDs
duplicate_absence = absence[absence.duplicated(subset=['absence_id'], keep=False)]
print("Duplicate absence IDs:\n", duplicate_absence)

# Check for duplicate performance IDs if you add performance dataset loading


# Save cleaned datasets to new CSV files
CLEAN_DATA_DIR = BASE_DIR / "clean_data"
CLEAN_DATA_DIR.mkdir(exist_ok=True)

employees.to_csv(CLEAN_DATA_DIR / "employees_clean.csv", index=False)
training.to_csv(CLEAN_DATA_DIR / "training_clean.csv", index=False)
absence.to_csv(CLEAN_DATA_DIR / "absence_clean.csv", index=False)

print("\nCleaned datasets saved to 'clean_data' folder.")
