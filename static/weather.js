// AgriHelper Secure Weather Service (Proxy-backed)
async function getWeather() {
    const cityInput = document.getElementById('city');
    const city = (cityInput ? cityInput.value : '').trim() || 'Pune';
    const errorEl = document.getElementById('error-message');
    const weatherInfoEl = document.getElementById('weather-info');
    const sevenDaysEl = document.getElementById('seven-days');

    if (errorEl) {
        errorEl.textContent = '';
        errorEl.classList.remove('visible');
    }

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (data.error) {
            if (errorEl) {
                errorEl.textContent = data.error.message || 'City not found! Please try another district.';
                errorEl.classList.add('visible');
            }
            return;
        }

        const current = data.current || {};
        const location = data.location || {};
        const advisory = data.agri_advisory || {};
        const iconUrl = current.condition?.icon?.startsWith('//') ? `https:${current.condition.icon}` : (current.condition?.icon || '');

        if (weatherInfoEl) {
            weatherInfoEl.innerHTML = `
                <div class="row align-items-center g-4 text-start">
                    <div class="col-md-5 text-center text-md-start">
                        <div class="d-flex align-items-center justify-content-center justify-content-md-start gap-3">
                            <img src="${iconUrl}" alt="${current.condition?.text || 'Weather'}" width="80" height="80">
                            <div>
                                <h2 class="display-5 fw-bold text-white mb-0">${current.temp_c}°C</h2>
                                <span class="text-secondary small">${current.temp_f}°F &bull; ${current.condition?.text || 'Clear'}</span>
                            </div>
                        </div>
                        <div class="mt-3">
                            <h4 class="text-white fw-bold mb-1"><i class="fa-solid fa-location-dot text-danger me-1"></i> ${location.name}, ${location.region || location.country}</h4>
                            <small class="text-secondary"><i class="fa-regular fa-clock me-1"></i> Local Time: ${location.localtime || 'Now'}</small>
                        </div>
                    </div>

                    <div class="col-md-7">
                        <div class="row g-2">
                            <div class="col-6">
                                <div class="p-3 bg-dark bg-opacity-75 rounded-3 border border-secondary border-opacity-25">
                                    <small class="text-secondary d-block"><i class="fa-solid fa-wind text-info me-1"></i> Wind Speed</small>
                                    <strong class="text-white fs-6">${current.wind_kph} km/h</strong>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-dark bg-opacity-75 rounded-3 border border-secondary border-opacity-25">
                                    <small class="text-secondary d-block"><i class="fa-solid fa-droplet text-primary me-1"></i> Relative Humidity</small>
                                    <strong class="text-white fs-6">${current.humidity}%</strong>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-dark bg-opacity-75 rounded-3 border border-secondary border-opacity-25">
                                    <small class="text-secondary d-block"><i class="fa-solid fa-cloud-rain text-success me-1"></i> Precipitation</small>
                                    <strong class="text-white fs-6">${current.precip_mm || 0} mm</strong>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="p-3 bg-dark bg-opacity-75 rounded-3 border border-secondary border-opacity-25">
                                    <small class="text-secondary d-block"><i class="fa-solid fa-sun text-warning me-1"></i> UV Index</small>
                                    <strong class="text-white fs-6">${current.uv || 5.0}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Agricultural Advisory Card -->
                <div class="mt-4 p-3 rounded-3 border border-success border-opacity-30 bg-success bg-opacity-10 text-start">
                    <h6 class="text-success fw-bold text-uppercase small mb-2">
                        <i class="fa-solid fa-seedling me-1"></i> On-Farm Weather Advisory:
                    </h6>
                    <div class="row g-2 small text-light">
                        <div class="col-md-6">
                            <div><i class="fa-solid fa-circle-check text-success me-1"></i> <strong>Spraying:</strong> ${advisory.spraying_note || 'Safe conditions'}</div>
                        </div>
                        <div class="col-md-6">
                            <div><i class="fa-solid fa-droplet text-info me-1"></i> <strong>Irrigation:</strong> ${advisory.irrigation_note || 'Monitor soil moisture'}</div>
                        </div>
                        <div class="col-md-6">
                            <div><i class="fa-solid fa-shield-virus text-warning me-1"></i> <strong>Pest/Fungal Risk:</strong> ${advisory.disease_risk || 'Low'}</div>
                        </div>
                        <div class="col-md-6">
                            <div><i class="fa-solid fa-wheat-awn text-warning me-1"></i> <strong>Harvest:</strong> ${advisory.harvest_condition || 'Optimal dry window'}</div>
                        </div>
                    </div>
                </div>
            `;
            weatherInfoEl.classList.add('visible');
        }

        // Render 7-day trend
        if (sevenDaysEl && data.history_7days) {
            let html = '<div class="row g-2">';
            data.history_7days.forEach(d => {
                html += `
                    <div class="col">
                        <div class="p-2 text-center bg-dark bg-opacity-75 rounded-3 border border-secondary border-opacity-25">
                            <small class="text-secondary d-block fw-bold">${d.day_name}</small>
                            <span class="text-white fw-bold d-block my-1">${d.avgtemp_c}°C</span>
                            <small class="text-muted" style="font-size: 0.7rem;">${d.date.slice(5)}</small>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            sevenDaysEl.innerHTML = html;
            sevenDaysEl.classList.add('visible');
        }

    } catch (err) {
        console.error("Weather fetch failed:", err);
        if (errorEl) {
            errorEl.textContent = 'Unable to connect to weather service. Please try again.';
            errorEl.classList.add('visible');
        }
    }
}

// Auto-load weather on page ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('weather-info')) {
        getWeather();
    }
});
