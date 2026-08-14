function toggleMenu() {
        const navLinks = document.getElementById('navLinks');
        navLinks.classList.toggle('active');
        }

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                const navLinks = document.getElementById('navLinks');
                navLinks.classList.remove('active');
            });
        });

async function getWeather() {
            const city = document.getElementById('city').value;
            const apiKey = 'f322870c8eb54fe48e6175526251703 ';  // Replace with your actual API key

            const urlCurrent = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${city}`;
            const urlHistory = `https://api.weatherapi.com/v1/history.json?key=${apiKey}&q=${city}&dt=`;

            // Clear previous error message
            document.getElementById('error-message').textContent = '';
            document.getElementById('error-message').classList.remove('visible');

            try {
                // Fetch current weather data
                const responseCurrent = await fetch(urlCurrent);
                const dataCurrent = await responseCurrent.json();

                if (dataCurrent.error) {
                    document.getElementById('error-message').textContent = 'City not found! Please try again.';
                    document.getElementById('error-message').classList.add('visible');
                    return;
                }

                const weatherCurrent = dataCurrent.current;
                const location = dataCurrent.location;

                let weatherDetails = `
                    <hr>
                    <div class="row">
                        <div class="column side">
                            <div class="containerforvalue2" style="margin-left:-7px">
                                <img src="https:${weatherCurrent.condition.icon}" alt="weather icon" width="100px">
                            </div>
                            <div class="containerforvalue2" style="margin-left:-7px">
                                <p><strong>Temperature:</strong><h3>${weatherCurrent.temp_c}°C / ${weatherCurrent.temp_f}°F</h3></p>
                            </div>
                            <p class="containerforvalue2" style="padding:35px;margin-left:-7px">${location.localtime}</p>
                        </div>
                        <div class="column middle">
                            <div class="containerforvalue2" style="margin-left:-7px"><h3>Weather in ${location.name}, ${location.country}</h3></div>
                            <div class="containerforvalue2" style="margin-left:-7px"><p><strong>Condition:</strong> ${weatherCurrent.condition.text}</p></div>
                            <div class="containerforvalue2" style="margin-left:-7px"><p><strong>Wind Speed:</strong> ${weatherCurrent.wind_kph} km/h (${weatherCurrent.wind_mph} mph)</p></div>
                            <div class="containerforvalue2" style="margin-left:-7px"><p><strong>Humidity:</strong> ${weatherCurrent.humidity}%</p></div>
                        </div>
                    </div>
                    <hr>
                `;

                // Add historical weather data for the last 6 days (temperature only)
                let temperatureData = [];
                let temperatureLabels = [];
                for (let i = 0; i < 6; i++) {
                    const date = new Date();
                    date.setDate(date.getDate() - i);
                    const dateString = date.toISOString().split('T')[0]; // Format: YYYY-MM-DD
                    const responseHistory = await fetch(`${urlHistory}${dateString}`);
                    const dataHistory = await responseHistory.json();

                    if (dataHistory.error) {
                        temperatureData.push(null);
                        temperatureLabels.push(dateString);
                        continue;
                    }

                    const dayWeather = dataHistory.forecast.forecastday[0].day;
                    temperatureData.push(dayWeather.avgtemp_c);
                    temperatureLabels.push(dateString);
                }

                // Display the historical temperature data in boxes
                let temperatureBoxData = [];
                temperatureLabels.forEach((label, index) => {
                    temperatureBoxData.push(`
                        <div class="day-box">
                            <p><strong>${label}</strong></p>
                            <hr width="100%" size="2">
                            <p>${temperatureData[index]}°C</p>
                        </div>
                    `);
                });
                document.getElementById('seven-days').innerHTML = temperatureBoxData.join('');

                // Combine current weather and historical data
                document.getElementById('weather-info').innerHTML = weatherDetails;

                // Add visible class to trigger animations
                setTimeout(() => {
                    document.getElementById('weather-info').classList.add('visible');
                    document.getElementById('seven-days').classList.add('visible');
                    document.querySelectorAll('.containerforvalue2').forEach(el => el.classList.add('visible'));
                    document.querySelectorAll('.day-box').forEach(el => el.classList.add('visible'));
                }, 100);

            } catch (error) {
                document.getElementById('error-message').textContent = 'Error retrieving weather data. Please try again later.';
                document.getElementById('error-message').classList.add('visible');
            }
        }
