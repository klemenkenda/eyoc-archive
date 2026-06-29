// Thin wrapper around Chart.js (loaded from CDN in index.html) for progression charts.
window.Eyoc = window.Eyoc || {};
Eyoc.lib = Eyoc.lib || {};

// steps: [{year, percentile, label}], ascending by year. Lower percentile = better
// result, so the y-axis is reversed (better results draw higher on the chart).
Eyoc.lib.renderPercentileChart = function (canvasEl, steps, existingChart) {
  if (existingChart) existingChart.destroy();
  if (!canvasEl || !steps.length) return null;
  return new Chart(canvasEl, {
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
            label: (ctx) => steps[ctx.dataIndex].label,
          },
        },
      },
    },
  });
};
