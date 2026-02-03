// Realistic total employee counts by department
const departmentEmployeeCounts = {
  IT: 30,
  Finance: 25,
  HR: 15,
  Operations: 20,
  Sales: 30,
};

// Realistic training completion counts per department
const trainingCompletionCounts = {
  IT: { completed: 25, notCompleted: 5 },
  Finance: { completed: 20, notCompleted: 5 },
  HR: { completed: 10, notCompleted: 5 },
  Operations: { completed: 18, notCompleted: 2 },
  Sales: { completed: 27, notCompleted: 3 },
};

// Sample employee dataset for averages
const employees = [
  { id: 'E001', department: 'IT', satisfaction: 8 },
  { id: 'E002', department: 'Finance', satisfaction: 7 },
  { id: 'E003', department: 'HR', satisfaction: 6 },
  { id: 'E004', department: 'Operations', satisfaction: 7 },
  { id: 'E005', department: 'Sales', satisfaction: 9 },
  { id: 'E006', department: 'IT', satisfaction: 7 },
];

// Sample absenteeism data by employee id
const absenteeismData = {
  'E001': 1,
  'E002': 3,
  'E003': 0,
  'E004': 2,
  'E005': 4,
  'E006': 1,
};

// Function to update KPI text by id
function updateKPI(id, value, suffix = "") {
  const el = document.getElementById(id);
  if (el) el.innerText = value + suffix;
}

// Calculate KPIs
function calculateKPIs(department) {
  let filteredEmployees;

  if (department === 'All') {
    filteredEmployees = employees;
  } else {
    filteredEmployees = employees.filter(emp => emp.department === department);
  }

  // Total employees from realistic counts
  const totalEmployees = department === 'All'
    ? Object.values(departmentEmployeeCounts).reduce((a, b) => a + b, 0)
    : (departmentEmployeeCounts[department] || 0);

  // Average satisfaction from sample data
  const avgSatisfaction = filteredEmployees.length > 0
    ? filteredEmployees.reduce((sum, emp) => sum + emp.satisfaction, 0) / filteredEmployees.length
    : 0;

  // Training completion percent from realistic data
  const trainingCounts = department === 'All'
    ? Object.values(trainingCompletionCounts).reduce(
        (acc, cur) => {
          acc.completed += cur.completed;
          acc.notCompleted += cur.notCompleted;
          return acc;
        },
        { completed: 0, notCompleted: 0 }
      )
    : (trainingCompletionCounts[department] || { completed: 0, notCompleted: 0 });

  const totalTrainings = trainingCounts.completed + trainingCounts.notCompleted;
  const trainingCompletion = totalTrainings > 0 ? (trainingCounts.completed / totalTrainings) * 100 : 0;

  // Average absenteeism from sample data
  const totalAbsences = filteredEmployees.reduce((sum, emp) => sum + (absenteeismData[emp.id] || 0), 0);
  const avgAbsenteeism = filteredEmployees.length > 0 ? totalAbsences / filteredEmployees.length : 0;

  return { totalEmployees, avgSatisfaction, trainingCompletion, avgAbsenteeism };
}

// Chart variables
let employeeDeptChart, trainingCompletionChart;

// Get department employee counts for bar chart
function getDepartmentChartData(selectedDept) {
  const departments = ['IT', 'Finance', 'HR', 'Operations', 'Sales'];

  if (selectedDept === 'All') {
    return departments.map(dep => departmentEmployeeCounts[dep] || 0);
  }

  return departments.map(dep => (dep === selectedDept ? departmentEmployeeCounts[dep] || 0 : 0));
}

// Get training completion data for pie chart
function getTrainingChartData(selectedDept) {
  if (selectedDept === 'All') {
    let totalCompleted = 0;
    let totalNotCompleted = 0;
    for (const dep in trainingCompletionCounts) {
      totalCompleted += trainingCompletionCounts[dep].completed;
      totalNotCompleted += trainingCompletionCounts[dep].notCompleted;
    }
    return [totalCompleted, totalNotCompleted];
  }

  if (trainingCompletionCounts[selectedDept]) {
    return [
      trainingCompletionCounts[selectedDept].completed,
      trainingCompletionCounts[selectedDept].notCompleted,
    ];
  }

  return [0, 0];
}

// Initialize charts
function initCharts() {
  const ctxDept = document.getElementById('employee-department-chart').getContext('2d');
  employeeDeptChart = new Chart(ctxDept, {
    type: 'bar',
    data: {
      labels: ['IT', 'Finance', 'HR', 'Operations', 'Sales'],
      datasets: [{
        label: 'Employees',
        data: getDepartmentChartData('All'),
        backgroundColor: 'rgba(0, 122, 204, 0.7)',
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Employee Count by Department' },
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 5 } },
      },
    },
  });

  const ctxTrain = document.getElementById('training-completion-chart').getContext('2d');
  trainingCompletionChart = new Chart(ctxTrain, {
    type: 'pie',
    data: {
      labels: ['Completed', 'Not Completed'],
      datasets: [{
        label: 'Training',
        data: getTrainingChartData('All'),
        backgroundColor: ['#007acc', '#cccccc'],
      }],
    },
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Training Completion Status' },
      },
    },
  });
}

// Update charts
function updateCharts(selectedDept) {
  employeeDeptChart.data.datasets[0].data = getDepartmentChartData(selectedDept);
  employeeDeptChart.update();

  trainingCompletionChart.data.datasets[0].data = getTrainingChartData(selectedDept);
  trainingCompletionChart.update();
}

// Update dashboard KPIs and charts
function updateDashboard(department) {
  const kpis = calculateKPIs(department);

updateKPI('total-employees', kpis.totalEmployees);
updateKPI('avg-satisfaction', kpis.avgSatisfaction.toFixed(1));
updateKPI('training-rate', kpis.trainingCompletion.toFixed(0), '%');  // fixed ID here
updateKPI('avg-absenteeism', kpis.avgAbsenteeism.toFixed(1));


  updateCharts(department);
}

// Department filter event listener
const departmentFilter = document.getElementById('department-filter');
departmentFilter.addEventListener('change', () => {
  updateDashboard(departmentFilter.value);
});

// Initialize everything on page load
window.onload = function () {
  initCharts();
  updateDashboard('All');
};
