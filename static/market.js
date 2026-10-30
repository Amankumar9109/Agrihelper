/**
 * AgriHelper Market Intelligence Engine
 * Handles APMC Pricing, Price Trend Charts, Mandi Drilldown & National Comparisons
 */

let stateChart = null;
let nationalChart = null;
let trendChart = null;
let currentTrendDays = 30;

document.addEventListener("DOMContentLoaded", () => {
  const stateDropdown = document.getElementById("stateDropdown");
  const districtDropdown = document.getElementById("districtDropdown");
  const marketDropdown = document.getElementById("marketDropdown");
  const commodityDropdown = document.getElementById("commodityDropdown");
  const getPricesBtn = document.getElementById("getPrices");

  // State dropdown change
  if (stateDropdown) {
    stateDropdown.addEventListener("change", () => {
      const state = stateDropdown.value;
      if (typeof onStateClick === "function") {
        // Highlight state on the map
        document.querySelectorAll(".india-state-path").forEach(p => p.classList.remove("active-state"));
        const statePath = document.querySelector(`.india-state-path[data-state="${state}"]`);
        if (statePath) statePath.classList.add("active-state");
      }
      fetchOptions("district", state, districtDropdown, "District");
      resetDropdown(marketDropdown, "Market");
      resetDropdown(commodityDropdown, "Commodity");
    });
  }

  // District dropdown change
  if (districtDropdown) {
    districtDropdown.addEventListener("change", () => {
      fetchOptions("market", districtDropdown.value, marketDropdown, "Market");
      resetDropdown(commodityDropdown, "Commodity");
    });
  }

  // Market dropdown change
  if (marketDropdown) {
    marketDropdown.addEventListener("change", () => {
      fetchOptions("commodity", marketDropdown.value, commodityDropdown, "Commodity");
    });
  }

  // Fetch prices button
  if (getPricesBtn) {
    getPricesBtn.addEventListener("click", showPricesAndCharts);
  }

  // Trend timeframe pills (7-day / 30-day)
  document.querySelectorAll(".trend-pill").forEach(btn => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".trend-pill").forEach(b => b.classList.remove("active"));
      e.target.classList.add("active");
      currentTrendDays = parseInt(e.target.getAttribute("data-days") || 30);
      fetchPriceTrends();
    });
  });
});

function fetchOptions(level, selection, dropdown, label) {
  if (!dropdown) return;
  dropdown.innerHTML = `<option selected disabled>Loading ${label}s...</option>`;

  fetch("/get_options", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level: level, selection: selection })
  })
    .then(res => res.json())
    .then(options => {
      dropdown.innerHTML = `<option selected disabled>Select ${label}</option>`;
      options.forEach(opt => {
        dropdown.innerHTML += `<option value="${opt}">${opt}</option>`;
      });
    })
    .catch(err => {
      console.error(`Error fetching ${level} options:`, err);
      dropdown.innerHTML = `<option selected disabled>Failed to load ${label}s</option>`;
    });
}

function resetDropdown(dropdown, label) {
  if (!dropdown) return;
  dropdown.innerHTML = `<option selected disabled>Select ${label}</option>`;
}

function showPricesAndCharts() {
  const state = document.getElementById("stateDropdown")?.value;
  const district = document.getElementById("districtDropdown")?.value;
  const market = document.getElementById("marketDropdown")?.value;
  const commodity = document.getElementById("commodityDropdown")?.value;

  if (!state || !district || !market || !commodity ||
      state.includes("Select") || district.includes("Select") ||
      market.includes("Select") || commodity.includes("Select")) {
    alert("Please select State, District, Market, and Commodity before analyzing prices.");
    return;
  }

  // Show loading indicator
  const outputContainer = document.getElementById("marketOutputContainer");
  if (outputContainer) outputContainer.style.display = "block";

  // Fetch current APMC prices
  fetch("/get_prices", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state, district, market, commodity })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }

      displayPriceData(data.prices, commodity, market, state);
      drawStateChart(data.state_comparison, market, commodity, state);
      drawNationalChart(data.national_comparison, commodity);

      // Also trigger 7/30-day Price Trend Chart
      fetchPriceTrends();
    })
    .catch(err => console.error("Error fetching prices:", err));
}

function displayPriceData(prices, commodity, market, state) {
  const minEl = document.getElementById("valMinPrice");
  const modalEl = document.getElementById("valModalPrice");
  const maxEl = document.getElementById("valMaxPrice");
  const bannerEl = document.getElementById("selectedMandiHeader");

  if (minEl) minEl.textContent = `₹${prices['Min Price']}`;
  if (modalEl) modalEl.textContent = `₹${prices['Modal Price']}`;
  if (maxEl) maxEl.textContent = `₹${prices['Max Price']}`;

  if (bannerEl) {
    bannerEl.innerHTML = `
      <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
        <div>
          <h4 class="mb-0 text-white font-weight-bold">${commodity} in ${market}</h4>
          <span class="text-muted small"><i class="fa-solid fa-map-pin me-1 text-success"></i>${state} &bull; Verified APMC Reporting</span>
        </div>
        <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill">
          <i class="fa-solid fa-circle-check me-1"></i> APMC Rate Active
        </span>
      </div>
    `;
  }
}

function fetchPriceTrends() {
  const state = document.getElementById("stateDropdown")?.value;
  const district = document.getElementById("districtDropdown")?.value;
  const market = document.getElementById("marketDropdown")?.value;
  const commodity = document.getElementById("commodityDropdown")?.value;

  if (!state || !commodity || state.includes("Select") || commodity.includes("Select")) return;

  fetch("/api/price-trends", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state, district, market, commodity, days: currentTrendDays })
  })
    .then(res => res.json())
    .then(trendData => {
      drawTrendChart(trendData);
    })
    .catch(err => console.error("Error fetching price trends:", err));
}

function drawTrendChart(trendData) {
  const canvas = document.getElementById("priceTrendChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  if (trendChart) trendChart.destroy();

  // Create subtle gradient fill for trend line
  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(74, 222, 128, 0.45)");
  gradient.addColorStop(1, "rgba(74, 222, 128, 0.0)");

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: trendData.dates,
      datasets: [
        {
          label: "Modal Price (₹/Qtl)",
          data: trendData.modal_prices,
          borderColor: "#4ade80",
          backgroundColor: gradient,
          borderWidth: 3,
          fill: true,
          tension: 0.35,
          pointRadius: trendData.dates.length > 15 ? 2 : 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#22c55e"
        },
        {
          label: "Max Price",
          data: trendData.max_prices,
          borderColor: "rgba(239, 68, 68, 0.4)",
          borderDash: [5, 5],
          borderWidth: 1.5,
          fill: false,
          pointRadius: 0
        },
        {
          label: "Min Price",
          data: trendData.min_prices,
          borderColor: "rgba(59, 130, 246, 0.4)",
          borderDash: [5, 5],
          borderWidth: 1.5,
          fill: false,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: { color: "#cbd5e1", font: { size: 11 } }
        },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleColor: "#4ade80",
          bodyColor: "#f8fafc",
          padding: 10,
          borderColor: "rgba(255, 255, 255, 0.1)",
          borderWidth: 1
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", maxTicksLimit: 10 }
        },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: {
            color: "#94a3b8",
            callback: (v) => `₹${v}`
          }
        }
      }
    }
  });

  // Update trend summary stats badge
  const trendBadge = document.getElementById("trendChangeBadge");
  if (trendBadge) {
    const isPos = trendData.change_pct >= 0;
    trendBadge.className = `badge ${isPos ? 'bg-success' : 'bg-danger'} px-2 py-1`;
    trendBadge.innerHTML = `<i class="fa-solid fa-arrow-trend-${isPos ? 'up' : 'down'} me-1"></i> ${isPos ? '+' : ''}${trendData.change_pct}% in last ${currentTrendDays} days`;
  }
}

function drawStateChart(stateComparison, selectedMarket, commodity, state) {
  const canvas = document.getElementById("stateMarketChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  if (stateChart) stateChart.destroy();

  const labels = Object.keys(stateComparison);
  const data = Object.values(stateComparison);

  const backgroundColors = labels.map(m =>
    m === selectedMarket ? "rgba(245, 158, 11, 0.9)" : "rgba(34, 197, 94, 0.6)"
  );

  stateChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: `${commodity} Price (₹/Qtl)`,
        data: data,
        backgroundColor: backgroundColors,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          callbacks: {
            label: (ctx) => `Modal Price: ₹${ctx.parsed.y} / Quintal`
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", maxRotation: 45, minRotation: 45 }
        },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: {
            color: "#94a3b8",
            callback: (v) => `₹${v}`
          }
        }
      }
    }
  });
}

function drawNationalChart(nationalComparison, commodity) {
  const canvas = document.getElementById("nationalChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  if (nationalChart) nationalChart.destroy();

  const labels = Object.keys(nationalComparison);
  const data = Object.values(nationalComparison);

  nationalChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: `National Price of ${commodity}`,
        data: data,
        borderColor: "#f59e0b",
        backgroundColor: "rgba(245, 158, 11, 0.15)",
        borderWidth: 2.5,
        fill: true,
        tension: 0.3,
        pointBackgroundColor: "#f59e0b",
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#94a3b8", maxRotation: 45, minRotation: 45 }
        },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: {
            color: "#94a3b8",
            callback: (v) => `₹${v}`
          }
        }
      }
    }
  });
}
