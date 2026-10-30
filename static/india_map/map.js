/**
 * Interactive D3/SVG India Map with Choropleth Heatmap and Mandi Intelligence
 */
let mapStateSummary = {};
let currentCommodity = "All";
let minPrice = 0;
let maxPrice = 0;
let selectedState = null;
let currentZoom = 1;
let panX = 0;
let panY = 0;
let isPanning = false;
let startX = 0;
let startY = 0;

document.addEventListener("DOMContentLoaded", () => {
  initIndiaMap();
  setupMapControls();
});

function initIndiaMap() {
  const container = document.getElementById("indiaMapContainer");
  if (!container || typeof INDIA_MAP_STATES === "undefined") return;

  // Clear previous SVG
  container.innerHTML = "";

  // Create SVG
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 650 720");
  svg.setAttribute("id", "indiaSvg");
  svg.classList.add("india-svg");

  // Create SVG Filters for subtle drop shadow and glow
  svg.innerHTML = `
    <defs>
      <filter id="stateShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
      </filter>
      <filter id="activeGlow" x="-30%" y="-30%" width="160%" height="160%">
        <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#4ade80" flood-opacity="0.9"/>
      </filter>
    </defs>
    <g id="mapViewport" class="map-viewport"></g>
  `;

  container.appendChild(svg);
  const viewport = svg.querySelector("#mapViewport");

  // Render States
  INDIA_MAP_STATES.forEach(st => {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", st.d);
    path.setAttribute("id", `state-${st.id}`);
    path.setAttribute("data-state", st.name);
    path.setAttribute("class", "india-state-path");
    path.setAttribute("filter", "url(#stateShadow)");

    // Tooltip events
    path.addEventListener("mouseenter", (e) => onStateHover(e, st.name));
    path.addEventListener("mousemove", (e) => moveTooltip(e));
    path.addEventListener("mouseleave", onStateLeave);
    path.addEventListener("click", () => onStateClick(st.name));

    viewport.appendChild(path);

    // Optional short label
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", st.labelX);
    text.setAttribute("y", st.labelY);
    text.setAttribute("class", "state-code-label");
    text.textContent = st.id;
    text.setAttribute("pointer-events", "none");
    viewport.appendChild(text);
  });

  // Fetch summary data and apply colors
  fetchStateSummary("All");
  setupPanZoom(svg, viewport);
}

function fetchStateSummary(commodity) {
  currentCommodity = commodity;
  const url = `/api/state-summary?commodity=${encodeURIComponent(commodity)}`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      mapStateSummary = data.states || {};
      minPrice = data.min_price || 0;
      maxPrice = data.max_price || 0;
      updateMapChoropleth();
      updateLegend(data);
    })
    .catch(err => console.error("Error fetching state summary:", err));
}

function updateMapChoropleth() {
  const paths = document.querySelectorAll(".india-state-path");

  paths.forEach(path => {
    const stateName = path.getAttribute("data-state");
    const info = mapStateSummary[stateName];

    if (!info || info.avg_modal_price === null || info.avg_modal_price === undefined) {
      path.style.fill = "#1e293b"; // Muted dark for no data
      path.setAttribute("data-has-data", "false");
    } else {
      path.setAttribute("data-has-data", "true");
      const color = getChoroplethColor(info.avg_modal_price, minPrice, maxPrice);
      path.style.fill = color;
    }
  });
}

function getChoroplethColor(val, min, max) {
  if (min === max || !val) return "#10b981"; // Safe green default
  const ratio = Math.max(0, Math.min(1, (val - min) / (max - min)));

  // Smooth color ramp: Emerald Green -> Amber Orange -> Coral Crimson
  if (ratio < 0.5) {
    const t = ratio * 2;
    // from #10b981 (16, 185, 129) to #f59e0b (245, 158, 11)
    const r = Math.round(16 + t * (245 - 16));
    const g = Math.round(185 + t * (158 - 185));
    const b = Math.round(129 + t * (11 - 129));
    return `rgb(${r}, ${g}, ${b})`;
  } else {
    const t = (ratio - 0.5) * 2;
    // from #f59e0b (245, 158, 11) to #ef4444 (239, 68, 68)
    const r = Math.round(245 + t * (239 - 245));
    const g = Math.round(158 + t * (68 - 158));
    const b = Math.round(11 + t * (68 - 11));
    return `rgb(${r}, ${g}, ${b})`;
  }
}

function updateLegend(data) {
  const minLabel = document.getElementById("legendMinPrice");
  const maxLabel = document.getElementById("legendMaxPrice");
  const legendTitle = document.getElementById("legendCommodityTitle");

  if (minLabel) minLabel.textContent = `₹${Math.round(data.min_price || 0)}`;
  if (maxLabel) maxLabel.textContent = `₹${Math.round(data.max_price || 0)}`;
  if (legendTitle) legendTitle.textContent = data.commodity === 'All' ? 'All Commodities (Avg ₹/Qtl)' : `${data.commodity} (Avg ₹/Qtl)`;
}

// Tooltip Handling
function onStateHover(e, stateName) {
  const tooltip = document.getElementById("indiaMapTooltip");
  if (!tooltip) return;

  const info = mapStateSummary[stateName] || {
    mandis: 0,
    avg_modal_price: "N/A",
    top_commodity: "N/A",
    total_records: 0
  };

  const priceDisplay = info.avg_modal_price && info.avg_modal_price !== "N/A"
    ? `₹${Math.round(info.avg_modal_price)} / Qtl`
    : `<span class="text-muted">No Mandi Data</span>`;

  tooltip.innerHTML = `
    <div class="tooltip-header">
      <i class="fa-solid fa-location-dot me-1 text-success"></i>
      <strong>${stateName}</strong>
    </div>
    <div class="tooltip-body">
      <div class="d-flex justify-content-between mb-1">
        <span>Active Mandis:</span>
        <strong class="text-light">${info.mandis}</strong>
      </div>
      <div class="d-flex justify-content-between mb-1">
        <span>Avg Modal Price:</span>
        <strong class="text-warning">${priceDisplay}</strong>
      </div>
      <div class="d-flex justify-content-between mb-1">
        <span>Top Commodity:</span>
        <strong class="text-info">${info.top_commodity}</strong>
      </div>
      <div class="d-flex justify-content-between">
        <span>Traded Lots:</span>
        <span class="badge bg-secondary">${info.total_records}</span>
      </div>
    </div>
    <div class="tooltip-footer">Click to inspect state mandis</div>
  `;

  tooltip.style.display = "block";
  moveTooltip(e);
}

function moveTooltip(e) {
  const tooltip = document.getElementById("indiaMapTooltip");
  if (!tooltip) return;

  const offset = 18;
  const x = e.clientX + offset;
  const y = e.clientY + offset;

  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

function onStateLeave() {
  const tooltip = document.getElementById("indiaMapTooltip");
  if (tooltip) tooltip.style.display = "none";
}

// State Selection via Map Click
function onStateClick(stateName) {
  selectedState = stateName;

  // Highlight state on map
  document.querySelectorAll(".india-state-path").forEach(p => {
    p.classList.remove("active-state");
  });

  const statePath = document.querySelector(`.india-state-path[data-state="${stateName}"]`);
  if (statePath) {
    statePath.classList.add("active-state");
  }

  // Update State Dropdown in Sidebar
  const stateDropdown = document.getElementById("stateDropdown");
  if (stateDropdown) {
    stateDropdown.value = stateName;

    // Trigger state change to populate districts
    const event = new Event("change");
    stateDropdown.dispatchEvent(event);
  }

  // Update selected state badge in sidebar
  const stateBadge = document.getElementById("activeStateBadge");
  if (stateBadge) {
    stateBadge.innerHTML = `<i class="fa-solid fa-location-crosshairs me-1 text-success"></i> Selected: <strong>${stateName}</strong>`;
    stateBadge.style.display = "inline-block";
  }

  // Scroll to sidebar on mobile
  if (window.innerWidth < 992) {
    const sidebar = document.getElementById("marketControlsSidebar");
    if (sidebar) sidebar.scrollIntoView({ behavior: 'smooth' });
  }
}

// Pan & Zoom Controls
function setupPanZoom(svg, viewport) {
  let isDragging = false;
  let startPanX = 0;
  let startPanY = 0;

  svg.addEventListener("mousedown", (e) => {
    if (e.target.classList.contains("india-state-path")) return; // Let clicks pass
    isDragging = true;
    startPanX = e.clientX - panX;
    startPanY = e.clientY - panY;
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    panX = e.clientX - startPanX;
    panY = e.clientY - startPanY;
    applyTransform(viewport);
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
  });

  // Wheel zoom
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    currentZoom = Math.min(3.5, Math.max(0.8, currentZoom * zoomFactor));
    applyTransform(viewport);
  });
}

function applyTransform(viewport) {
  if (viewport) {
    viewport.setAttribute("transform", `translate(${panX}, ${panY}) scale(${currentZoom})`);
  }
}

function setupMapControls() {
  const zoomInBtn = document.getElementById("mapZoomIn");
  const zoomOutBtn = document.getElementById("mapZoomOut");
  const resetBtn = document.getElementById("mapResetZoom");
  const commodityFilter = document.getElementById("mapCommodityFilter");

  const viewport = document.getElementById("mapViewport");

  if (zoomInBtn) {
    zoomInBtn.addEventListener("click", () => {
      currentZoom = Math.min(3.5, currentZoom * 1.25);
      applyTransform(viewport);
    });
  }

  if (zoomOutBtn) {
    zoomOutBtn.addEventListener("click", () => {
      currentZoom = Math.max(0.8, currentZoom / 1.25);
      applyTransform(viewport);
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      currentZoom = 1;
      panX = 0;
      panY = 0;
      applyTransform(viewport);
    });
  }

  if (commodityFilter) {
    commodityFilter.addEventListener("change", (e) => {
      fetchStateSummary(e.target.value);
    });
  }
}
