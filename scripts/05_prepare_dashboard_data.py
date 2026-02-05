import pandas as pd
from pathlib import Path
import json

# Define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DATA_DIR = BASE_DIR / "clean_data"
OUTPUT_DIR = BASE_DIR / "dashboard_data"
OUTPUT_DIR.mkdir(exist_ok=True)  # Create output folder if it doesn't exist

# Load cleaned datasets
employees = pd.read_csv(CLEAN_DATA_DIR / "employees_clean.csv")
absence = pd.read_csv(CLEAN_DATA_DIR / "absence_clean.csv")
training = pd.read_csv(CLEAN_DATA_DIR / "training_clean.csv")

# --- Calculate Key Performance Indicators (KPIs) ---

# Total unique employees
total_employees = employees['employee_id'].nunique()

# Average satisfaction score (rounded to 2 decimals)
avg_satisfaction = round(absence['satisfaction_score'].mean(), 2)

# Training completion rate (%) - proportion of 'Completed' training status
training_completion_rate = round(
    (training['completion_status'] == 'Completed').mean() * 100, 2
)

# Average absenteeism rate (total days absent divided by total employees)
absence_days_total = absence['days_absent'].sum()
absence_rate = round(absence_days_total / total_employees, 2)

# Pack KPIs into a dictionary for JSON export
kpis = {
    "total_employees": total_employees,
    "avg_satisfaction": avg_satisfaction,
    "training_completion_rate": training_completion_rate,
    "absence_rate": absence_rate
}

# Save KPIs as JSON file for dashboard consumption
with open(OUTPUT_DIR / "kpis.json", "w") as f:
    json.dump(kpis, f)

# --- Prepare Data for Visualization ---

# Calculate headcount by department for dashboard charting
headcount_by_dept = employees.groupby('department').size().reset_index(name='count')

# Export headcount data to JSON format
headcount_by_dept.to_json(OUTPUT_DIR / "headcount_by_dept.json", orient='records')

print("Dashboard data preparation completed successfully. Files saved in 'dashboard_data' folder.")
