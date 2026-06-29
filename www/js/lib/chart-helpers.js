// Thin wrapper around Chart.js (loaded from CDN in index.html) for progression charts.
window.Eyoc = window.Eyoc || {};
Eyoc.lib = Eyoc.lib || {};

// steps: [{year, percentile, label}], ascending by year. Lower percentile = better
// result, so the y-axis is reversed (better results draw higher on the chart).
//
// Reuses existingChart in place (just swapping its data) when it's still attached to
// the same canvas, rather than destroy()-ing and creating a new Chart every time a
// filter changes. Destroying and immediately recreating a chart on the same canvas
// races with Chart.js's own pending resize/draw callback from the previous instance
// (a known Chart.js timing issue) and can leave the new chart half-drawn/blank even
// though a Chart instance was successfully constructed. The tooltip label callback
// reads from chart._eyocSteps (kept in sync on every update) instead of closing over
// the steps array directly, since in-place updates can't replace that closure.
Eyoc.lib.renderPercentileChart = function (canvasEl, steps, existingChart) {
  if (!canvasEl || !steps.length) {
    if (existingChart) existingChart.destroy();
    return null;
  }

  if (existingChart && existingChart.canvas === canvasEl) {
    existingChart._eyocSteps = steps;
    existingChart.data.labels = steps.map((s) => s.year);
    existingChart.data.datasets[0].data = steps.map((s) => s.percentile);
    existingChart.update();
    return existingChart;
  }

  if (existingChart) existingChart.destroy();
  const chart = new Chart(canvasEl, {
    type: "line",
    data: {
      labels: steps.map((s) => s.year),
      datasets: [
        {
          label: "Percentile (lower = better)",
          data: steps.map((s) => s.percentile),
          borderColor: "#1f4e8c",
          backgroundColor: "#1f4e8c",
          tension: 0.15,
          pointRadius: 4,
        },
      ],
    },
    options: {
      scales: {
        y: {
          reverse: true,
          min: 0,
          max: 100,
          title: { display: true, text: "Percentile (%)" },
        },
        x: { title: { display: true, text: "Year" } },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx) => chart._eyocSteps[ctx.dataIndex].label,
          },
        },
      },
    },
  });
  chart._eyocSteps = steps;
  return chart;
};
