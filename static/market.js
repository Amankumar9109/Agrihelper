let stateChart = null;
let nationalChart = null;

document.addEventListener("DOMContentLoaded", () => {
  const stateDropdown = document.getElementById("stateDropdown");
  const districtDropdown = document.getElementById("districtDropdown");
  const marketDropdown = document.getElementById("marketDropdown");
  const commodityDropdown = document.getElementById("commodityDropdown");

  // Set up dropdown change handlers
  stateDropdown.addEventListener("change", () => {
    fetchOptions("district", stateDropdown.value, districtDropdown, "District");
    resetDropdown(marketDropdown, "Market");
    resetDropdown(commodityDropdown, "Commodity");
  });

  districtDropdown.addEventListener("change", () => {
    fetchOptions("market", districtDropdown.value, marketDropdown, "Market");
    resetDropdown(commodityDropdown, "Commodity");
  });

  marketDropdown.addEventListener("change", () => {
    fetchOptions("commodity", marketDropdown.value, commodityDropdown, "Commodity");
  });

  document.getElementById("getPrices").addEventListener("click", showPricesAndCharts);
});

// Fetch options for next dropdown based on selection
function fetchOptions(level, selection, dropdown, label) {
  fetch("/get_options", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ level: level, selection: selection })
  })
    .then(res => res.json())
    .then(options => {
      dropdown.innerHTML = `<option selected disabled>Select ${label}</option>`;
      options.forEach(opt => {
        dropdown.innerHTML += `<option value="${opt}">${opt}</option>`;
      });
    })
    .catch(err => console.error(`Error fetching ${level} options:`, err));
}

// Reset lower dropdowns when parent changes
function resetDropdown(dropdown, label) {
  dropdown.innerHTML = `<option selected disabled>Select ${label}</option>`;
}

function showPricesAndCharts() {
  const state = document.getElementById("stateDropdown").value;
  const district = document.getElementById("districtDropdown").value;
  const market = document.getElementById("marketDropdown").value;
  const commodity = document.getElementById("commodityDropdown").value;

  if (!state || !district || !market || !commodity) {
    alert("Please select all options before fetching prices.");
    return;
  }

  fetch("/get_prices", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ state, district, market, commodity })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }

      displayPriceData(data.prices);
      drawStateChart(data.state_comparison, market, commodity, state);
      drawNationalChart(data.national_comparison, commodity);
    })
    .catch(err => console.error("Error fetching prices:", err));
}

function displayPriceData(prices) {
  document.getElementById("priceData").innerHTML = `
    <h3>Price Info</h3>
    <p><strong>Min Price:</strong> ₹${prices['Min Price']}</p>
    <p><strong>Max Price:</strong> ₹${prices['Max Price']}</p>
    <p><strong>Modal Price:</strong> ₹${prices['Modal Price']}</p>
  `;
}

function drawStateChart(stateComparison, selectedMarket, commodity, state) {
  if (stateChart) stateChart.destroy();

  const labels = Object.keys(stateComparison);
  const data = Object.values(stateComparison);

  const backgroundColors = labels.map(market =>
    market === selectedMarket ? 'rgba(255, 99, 132, 0.7)' : 'rgba(54, 162, 235, 0.7)'
  );

  const ctx = document.getElementById("stateMarketChart").getContext("2d");
  stateChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: `${commodity} Prices in ${state}`,
        data: data,
        backgroundColor: backgroundColors
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function drawNationalChart(nationalComparison, commodity) {
  if (nationalChart) nationalChart.destroy();

  const labels = Object.keys(nationalComparison);
  const data = Object.values(nationalComparison);

  const ctx = document.getElementById("nationalChart").getContext("2d");
  nationalChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: `Price of ${commodity} across States`,
        data: data,
        borderColor: 'rgba(255, 159, 64, 0.9)',
        fill: false,
        tension: 0.2
      }]
    },
    options: {
      responsive: true
    }
  });
}

