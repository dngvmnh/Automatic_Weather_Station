    document.addEventListener('DOMContentLoaded', () => {
        const dateElement = document.querySelector('.date');
        const tempElement = document.querySelector('.temp');
        const weatherContentElement = document.querySelector('.weather-content');
        const weatherDescriptionElement = document.querySelector('.weather-description');
        const tempFormatElement = document.querySelector('.temp-format');
        const aqiValueElement = document.querySelector('.aqi-value');
        const pollutantElements = {
        co: document.querySelector('.co'),
        no: document.querySelector('.no'),
        no2: document.querySelector('.no2'),
        o3: document.querySelector('.o3'),
        so2: document.querySelector('.so2'),
        pm2_5: document.querySelector('.pm2_5'),
        pm10: document.querySelector('.pm10'),
        nh3: document.querySelector('.nh3')
        };
    
        const apiKey = '98d48501649a41790e957711ea3b6d24';
        const city = 'Ho Chi Minh City';
        const weatherApiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;
        const lat = 10.8231;
        const lon = 106.6297;
        const airPollutionApiUrl = `https://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${lon}&appid=${apiKey}`;
    
        function updateDate() {
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        const formattedDate = now.toLocaleDateString('en-US', options);
        dateElement.textContent = formattedDate;
        }
    
        function updateWeather() {
        fetch(weatherApiUrl)
            .then(response => response.json())
            .then(data => {
            const temperature = data.main.temp;
            const tempMax = data.main.temp_max;
            const tempMin = data.main.temp_min;
            const weatherCondition = data.weather[0].main;
            const weatherDescription = data.weather[0].description;
    
            tempElement.innerHTML = `${temperature.toFixed(1)}°C`;
            tempFormatElement.innerHTML = `High/Low: ${tempMax.toFixed(1)}°C / ${tempMin.toFixed(1)}°C`;
            weatherContentElement.innerHTML = `${weatherCondition} (${weatherDescription.charAt(0).toUpperCase() + weatherDescription.slice(1)})`;
            })
            .catch(error => {
            console.error('Error fetching weather data:', error);
            tempElement.innerHTML = 'Temp not available';
            tempFormatElement.innerHTML = 'High/Low: N/A / N/A';
            weatherContentElement.innerHTML = 'Weather not available';
            });
        }
        
        function updateAirQuality() {
        fetch(airPollutionApiUrl)
            .then(response => response.json())
            .then(data => {
            const aqi = data.list[0].main.aqi;
            const components = data.list[0].components;
    
            aqiValueElement.innerHTML = `AQI Level: <span class="aqi-number">${aqi}</span>`;
    
            const aqiNumberElement = document.querySelector('.aqi-number');
            aqiNumberElement.classList.remove('value-1', 'value-2', 'value-3', 'value-4', 'value-5');
            aqiNumberElement.classList.add(`value-${aqi}`);
    
            pollutantElements.co.innerHTML = `${components.co.toFixed(1)} µg/m³`;
            pollutantElements.no.innerHTML = `${components.no.toFixed(1)} µg/m³`;
            pollutantElements.no2.innerHTML = `${components.no2.toFixed(1)} µg/m³`;
            pollutantElements.o3.innerHTML = `${components.o3.toFixed(1)} µg/m³`;
            pollutantElements.so2.innerHTML = `${components.so2.toFixed(1)} µg/m³`;
            pollutantElements.pm2_5.innerHTML = `${components.pm2_5.toFixed(1)} µg/m³`;
            pollutantElements.pm10.innerHTML = `${components.pm10.toFixed(1)} µg/m³`;
            pollutantElements.nh3.innerHTML = `${components.nh3.toFixed(1)} µg/m³`;
            })
            .catch(error => {
            console.error('Error fetching air quality data:', error);
            aqiValueElement.innerHTML = 'AQI data not available';
            Object.keys(pollutantElements).forEach(key => {
                pollutantElements[key].innerHTML = 'N/A';
            });
            });
        }
    
        updateDate();
        updateWeather();
        updateAirQuality();
    
        setInterval(updateDate, 60000);
        setInterval(updateWeather, 60000);
        setInterval(updateAirQuality, 60000);
    });
    