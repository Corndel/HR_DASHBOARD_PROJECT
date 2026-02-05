// Scaled headcount (realistic organisation)
const headcount = {
  IT: 35,
  Finance: 25,
  HR: 20,
  Operations: 20
};

// KPI ratios per department
const kpisByDept = {
  All: { satisfaction: 7.17, training: 66.67, absence: 2.75 },
  IT: { satisfaction: 7.5, training: 70, absence: 3 },
  Finance: { satisfaction: 6.9, training: 65, absence: 2.5 },
  HR: { satisfaction: 7.0, training: 60, absence: 2.2 },
  Operations: { satisfaction: 7.2, training: 67, absence: 3.1 },
};

// Performance data
const performanceByDept = {
  All: { Excellent: 30, Good: 45, Average: 20, Poor: 5 },
  IT: { Excellent: 15, Good: 10, Average: 7, Poor: 3 },
  Finance: { Excellent: 7, Good: 10, Average: 6, Poor: 2 },
  HR: { Excellent: 5, Good: 9, Average: 4, Poor: 2 },
  Operations: { Excellent: 6, Good: 9, Average: 3, Poor: 2 }
};

// Employment type data
const employmentByDept = {
  All: { "Full-Time": 70, "Part-Time": 20, "Contractor": 10 },
  IT: { "Full-Time": 25, "Part-Time": 5, "Contractor": 5 },
  Finance: { "Full-Time": 20, "Part-Time": 5, "Contractor": 0 },
  HR: { "Full-Time": 15, "Part-Time": 5, "Contractor": 0 },
  Operations: { "Full-Time": 10, "Part-Time": 5, "Contractor": 5 },
};



// Gender distribution data
const genderByDept = {
  All: { Male: 55, Female: 45 },
  IT: { Male: 25, Female: 10 },
  Finance: { Male: 12, Female: 13 },
  HR: { Male: 6, Female: 14 },
  Operations: { Male: 12, Female: 8 }
};

// Chart descriptions
const trainingDescriptions = {
  All: "Shows number of employees who completed mandatory training.",
  IT: "Training completion for IT employees.",
  Finance: "Training completion for Finance employees.",
  HR: "Training completion for HR employees.",
  Operations: "Training completion for Operations employees."
};

const performanceDescriptions = {
  All: "Employee performance ratings across all departments.",
  IT: "Performance ratings for IT department.",
  Finance: "Performance ratings for Finance department.",
  HR: "Performance ratings for HR department.",
  Operations: "Performance ratings for Operations department."
};

let charts = {};

// KPI updater
function updateKPIs(dept) {
  const total =
    dept === "All"
      ? Object.values(headcount).reduce((a, b) => a + b, 0)
      : headcount[dept];

  const current = kpisByDept[dept] || kpisByDept.All;

  document.getElementById("kpi-headcount").innerText = total;
  document.getElementById("kpi-satisfaction").innerText = current.satisfaction.toFixed(2);
  document.getElementById("kpi-training").innerText = current.training.toFixed(0) + "%";
  document.getElementById("kpi-absence").innerText = current.absence.toFixed(1);
}

// Performance risk helper
function getRiskData(dept) {
  const perf = performanceByDept[dept] || performanceByDept.All;
  return [
    perf.Excellent + perf.Good,
    perf.Average + perf.Poor
  ];
}

// Init charts
function initCharts() {

 // Gender distribution 
const genderChart = document.getElementById("genderChart");

charts.gender = new Chart(genderChart, {
  type: "bar",
  data: {
    labels: ["Male", "Female"],
    datasets: [{
      data: Object.values(genderByDept.All),
      backgroundColor: ["#0a6ed1", "#f39c12"]
    }]
  },
  options: {
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true }
    }
  }
});



  charts.training = new Chart(trainingChart, {
    type: "doughnut",
    data: {
      labels: ["Completed", "Not Completed"],
      datasets: [{
        data: [kpisByDept.All.training, 100 - kpisByDept.All.training],
        backgroundColor: ["#0a6ed1", "#d0d0d0"]
      }]
    }
  });

  charts.performance = new Chart(performanceChart, {
    type: "bar",
    data: {
      labels: Object.keys(performanceByDept.All),
      datasets: [{
        data: Object.values(performanceByDept.All),
        backgroundColor: "#2ecc71"
      }]
    },
    options: { plugins: { legend: { display: false } } }
  });

  charts.employment = new Chart(employmentChart, {
    type: "pie",
    data: {
      labels: Object.keys(employmentByDept.All),
      datasets: [{
        data: Object.values(employmentByDept.All)
      }]
    }
  });
}

// Filter handler
document.getElementById("departmentFilter").addEventListener("change", e => {
  const dept = e.target.value;

  updateKPIs(dept);
const genderData = genderByDept[dept] || genderByDept.All;
charts.gender.data.datasets[0].data = Object.values(genderData);
charts.gender.update();

  const trainingVal = (kpisByDept[dept] || kpisByDept.All).training;
  charts.training.data.datasets[0].data = [trainingVal, 100 - trainingVal];
  charts.training.update();

  const perf = performanceByDept[dept] || performanceByDept.All;
  charts.performance.data.datasets[0].data = Object.values(perf);
  charts.performance.update();

  const emp = employmentByDept[dept] || employmentByDept.All;
  charts.employment.data.datasets[0].data = Object.values(emp);
  charts.employment.update();

  document.getElementById("trainingChartDesc").innerText =
    trainingDescriptions[dept] || trainingDescriptions.All;

  document.getElementById("performanceChartDesc").innerText =
    performanceDescriptions[dept] || performanceDescriptions.All;
});

// Load
window.onload = () => {
  initCharts();
  updateKPIs("All");
  document.getElementById("trainingChartDesc").innerText = trainingDescriptions.All;
  document.getElementById("performanceChartDesc").innerText = performanceDescriptions.All;
};
