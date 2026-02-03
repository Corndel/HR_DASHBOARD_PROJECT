import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DATA_DIR = BASE_DIR / "clean_data"
OUTPUT_DIR = BASE_DIR / "dashboard_data"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load cleaned data
employees = pd.read_csv(CLEAN_DATA_DIR / "employees_clean.csv")
absence = pd.read_csv(CLEAN_DATA_DIR / "absence_clean.csv")
training = pd.read_csv(CLEAN_DATA_DIR / "training_clean.csv")

# KPI 1: Total Employees
total_employees = employees['employee_id'].nunique()

# KPI 2: Average Satisfaction Score (rounded 2 decimals)
avg_satisfaction = round(absence['satisfaction_score'].mean(), 2)

# KPI 3: Training Completion Rate (%)
training_completion_rate = round(
    (training['completion_status'] == 'Completed').mean() * 100, 2)

# KPI 4: Absenteeism Rate (avg days absent per employee)
absence_days_total = absence['days_absent'].sum()
absence_rate = round(absence_days_total / total_employees, 2)

# Save KPIs to JSON
kpis = {
    "total_employees": total_employees,
    "avg_satisfaction": avg_satisfaction,
    "training_completion_rate": training_completion_rate,
    "absence_rate": absence_rate
}

with open(OUTPUT_DIR / "kpis.json", "w") as f:
    json.dump(kpis, f)


# Also prepare data for charts: headcount by department
headcount_by_dept = employees.groupby('department').size().reset_index(name='count')
headcount_by_dept.to_json(OUTPUT_DIR / "headcount_by_dept.json", orient='records')

print("Dashboard data prepared and saved to 'dashboard_data' folder.")





