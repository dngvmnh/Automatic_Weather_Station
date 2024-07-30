document.addEventListener('DOMContentLoaded', () => {
    const dateElement = document.querySelector('.date');
    const tempElement = document.querySelector('.temp');
    const weatherContentElement = document.querySelector('.weather-content');
  
    const apiKey = '98d48501649a41790e957711ea3b6d24';
    const city = 'Ho Chi Minh City'; 
    const weatherApiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;
  
    function updateDate() {
      fetch('http://worldtimeapi.org/api/timezone/Etc/UTC')
        .then(response => response.json())
        .then(data => {
          const currentDateTime = new Date(data.datetime);
          const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
          const formattedDate = currentDateTime.toLocaleDateString('en-US', options);
          dateElement.textContent = formattedDate;
        })
        .catch(error => {
          console.error('Error fetching date:', error);
          dateElement.textContent = 'Date not available';
        });
    }
  
    function updateWeather() {
      fetch(weatherApiUrl)
        .then(response => response.json())
        .then(data => {
          const temperature = data.main.temp;
          const weatherCondition = data.weather[0].main;
  
          tempElement.innerHTML = `${temperature.toFixed(1)}°C`;
          weatherContentElement.textContent = weatherCondition;
        })
        .catch(error => {
          console.error('Error fetching weather data:', error);
          tempElement.innerHTML = 'Temp not available';
          weatherContentElement.textContent = 'Weather not available';
        });
    }
  
    updateDate();
    updateWeather();
  
    setInterval(updateDate, 60000);
    
    setInterval(updateWeather, 3600000);
  });
  