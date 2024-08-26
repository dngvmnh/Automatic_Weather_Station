# Tutorial - Automatic Weather Station

## Requirements:

- ESP32
- Laptop
- USB wire
- DF Robot Environment Sensor
- Adapter
- Strong wifi
- Basic Python and HTML (optional) language
- Thonny Desktop
- Thingspeak account

# Step by step

---

# Dowload app

- Download Thonny
    
    [https://thonny.org/](https://thonny.org/)
    
- Create account Thingspeak
    
    [Single Sign On - ThingSpeak IoT](https://thingspeak.com/login)
    

# 1. Hardware setup

- Thonny setup
    - Connect your ESP32 to your laptop through USB or Type C wire
    - Open Thonny and choose run and choose “Configure interpreter”
    
    ![Config interpreter](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Config_interpreter.png))
    
    - Choose microPython and port that your laptop connect to ESP32
    - Click “Install or update Micropython” to download firmware to ESP32 (so that ESP32 can run Thonny code (Python))
    
    ![Install_firmware_esp32](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Install_firmware_esp32.png))
    
- Connect DF Robot Environmental sensor to I2C port in shell of ESP32

# 2. Software setup

- Install Thonny IDE
- Create Thingspeak account and create channel
    
    ![Create channel](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Create_channel.png))
    

# 3. Thingspeak setup

- Create a channel
- Name a channel and choose field for your project (max: 8 fields). Save channel
    
    ![Create channel](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Create_channel.png))
    
- Remember the channel id. Note: The id is different in every channel so check the channel id carefully
    
    ![Create channel and choose fields](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Create_channels_choose_fields.png))
    
- Sharing the project to public view so everyone can see it.
    
    ![Share channel](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/Share_channels.png))
    
- Check and remember the API KEYS for read and write
    
     ![API Keys](https://github.com/henrytran412/Automatic_Weather_Station_Guide/raw/main/Pictures/API_keys.png))
    

# 4. Python code

- Code
    
    ```python
    import machine
    import urequests
    import ujson as json
    import time
    import network
    
    # Define the I2C address and communication modes
    I2C_MODE = 0x01
    UART_MODE = 0x02
    DEV_ADDRESS = 0x22
    
    HPA = 0x01
    KPA = 0x02
    TEMP_C = 0x03
    TEMP_F = 0x04
    
    #Thông tin tài khoản Thingspeak 
    HTTP_HEADERS = {'Content-Type': 'application/json'} 
    THINGSPEAK_WRITE_API_KEY = 'CECWK4EDQD9CRCJW'
    THINGSPEAK_CHANNEL_ID= '2604448'
    THINGSPEAK_READ_API_KEY = 'UQNBZGODZAF499TP'
    USER_API_KEY = 'MQHY981MRKM29ZDE'
    
    ssid='MakerLab.vn' #tên mạng wifi
    password='' #password wifi
    
    # Cài đặt kết nối wifi
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
         pass
    print('network config:', sta_if.ifconfig())
    #xoa du lieu cu
    '''url = f'https://api.thingspeak.com/channels/2604448/feeds.json?api_key=MQHY981MRKM29ZDE'
    response = urequests.delete(url, headers={'Content-Type': 'application/json', 'api_key': USER_API_KEY})
    
    # Check the response
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    
    if response.status_code == 200:
        print('ThingSpeak data cleared successfully')
    else:
        print('Failed to clear ThingSpeak data')
    
    response.close()'''
    
    field1_request = 'https://api.thingspeak.com/channels/2604448/fields/1/last.json'
    
    class DFRobot_Environmental_Sensor():
        def __init__(self, i2cbus=None, baud=9600):
            self.i2cbus = i2cbus
            self._baud = baud
            self._uart_i2c = I2C_MODE if i2cbus else UART_MODE
            self._addr = None
    
        def _detect_device_address(self):
            rbuf = self._read_reg(0x04, 2)
            if self._uart_i2c == I2C_MODE:
                data = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                data = rbuf[0]
            return data
    
        def begin(self):
            if self._detect_device_address() != DEV_ADDRESS:
                return False
            return True
    
        def _read_reg(self, reg_addr, length):
            try:
                if self._uart_i2c == I2C_MODE:
                    rslt = self.i2cbus.readfrom_mem(self._addr, reg_addr, length)
                elif self._uart_i2c == UART_MODE:
                    # Implement UART read here if needed
                    rslt = [-1] * length
            except Exception as e:
                print("Error reading register:", e)
                rslt = [-1] * length
            return rslt
    
        def get_temperature(self, units):
            rbuf = self._read_reg(0x14, 2)
            if self._uart_i2c == I2C_MODE:
                data = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                data = rbuf[0]
            temp = (-45) + ((data * 175.00) / 1024.00 / 64.00)
            if units == TEMP_F:
                temp = temp * 1.8 + 32
            return round(temp, 2)
    
        def get_humidity(self):
            rbuf = self._read_reg(0x16, 2)
            if self._uart_i2c == I2C_MODE:
                humidity = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                humidity = rbuf[0]
            humidity = (humidity / 1024) * 100 / 64
            return humidity
    
        def get_ultraviolet_intensity(self):
            version = self._read_reg(0x05, 2)
            if (version[0] << 8 | version[1]) == 0x1001:
                rbuf = self._read_reg(0x10, 2)
                data = rbuf[0] << 8 | rbuf[1]
                ultraviolet = data / 1800
            else:
                rbuf = self._read_reg(0x10, 2)
                if self._uart_i2c == I2C_MODE:
                    data = rbuf[0] << 8 | rbuf[1]
                elif self._uart_i2c == UART_MODE:
                    data = rbuf[0]
                outputVoltage = 3.0 * data / 1024
                ultraviolet = abs((outputVoltage - 0.99) * (15.0 - 0.0) / (2.9 - 0.99) + 0.0)/25
            return round(ultraviolet, 2)
    
        def get_luminousintensity(self):
            rbuf = self._read_reg(0x12, 2)
            if self._uart_i2c == I2C_MODE:
                data = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                data = rbuf[0]
            luminous = data * (1.0023 + data * (8.1488e-5 + data * (-9.3924e-9 + data * 6.0135e-13)))
            return round(luminous, 2)
    
        def get_atmosphere_pressure(self, units):
            rbuf = self._read_reg(0x18, 2)
            if self._uart_i2c == I2C_MODE:
                atmosphere = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                atmosphere = rbuf[0]
            if units == KPA:
                atmosphere /= 10
            return atmosphere
    
        def get_elevation(self):
            rbuf = self._read_reg(0x18, 2)
            if self._uart_i2c == I2C_MODE:
                elevation = rbuf[0] << 8 | rbuf[1]
            elif self._uart_i2c == UART_MODE:
                elevation = rbuf[0]
            elevation = 44330 * (1.0 - pow(elevation / 1015.0, 0.1903))
            return round(elevation, 2)
    
    class DFRobot_Environmental_Sensor_I2C(DFRobot_Environmental_Sensor):
        def __init__(self, i2cbus, addr):
            super().__init__(i2cbus)
            self._addr = addr
    
        def _read_reg(self, reg_addr, length):
            return self.i2cbus.readfrom_mem(self._addr, reg_addr, length)
    
    class DFRobot_Environmental_Sensor_UART(DFRobot_Environmental_Sensor):
        def __init__(self, baud, addr):
            super().__init__(None, baud)
            self._addr = addr
            # Initialize UART here if needed
    
        def _read_reg(self, reg_addr, length):
            # Implement UART read here if needed
            return [-1] * length
    
    def setup():
        i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
        sensor = DFRobot_Environmental_Sensor_I2C(i2c, DEV_ADDRESS)
        
        if not sensor.begin():
            print("Sensor initialization failed!!")
            return
    
        print("Sensor initialization success!!")
    
        while True:
            temperature_c = sensor.get_temperature(TEMP_C)
            temperature_f = sensor.get_temperature(TEMP_F)
            humidity = sensor.get_humidity()
            ultraviolet_intensity = sensor.get_ultraviolet_intensity()
            luminous_intensity = sensor.get_luminousintensity()
            atmospheric_pressure = sensor.get_atmosphere_pressure(HPA)
            elevation = sensor.get_elevation()
            
            print("-----------------------")
            print("Temp: " + str(temperature_c) + " °C")
            print("Temp: " + str(temperature_f) + " °F")
            print("Humidity: " + str(humidity) + " %")
            print("Ultraviolet intensity: " + str(ultraviolet_intensity) + " mw/cm2")
            print("Luminous Intensity: " + str(luminous_intensity) + " lx")
            print("Atmospheric pressure: " + str(atmospheric_pressure) + " hPa")
            print("Elevation: " + str(elevation) + " m")
            print("-----------------------")
            
            sensor_reading = {'field1':temperature_c, 'field2':humidity, 'field3':ultraviolet_intensity, 'field4':luminous_intensity, 'field5':atmospheric_pressure, 'field6': elevation}
            print(sensor_reading) #in 2 giá trị gửi
            request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,json = sensor_reading, headers = HTTP_HEADERS )  
            request.close()
            time.sleep(1)
    
    if __name__ == "__main__":
        setup()
     
    
    ```
    
- Explain
    - **Imports and Configuration**
        
        ```python
        import machine
        import urequests
        import ujson as json
        import time
        import network
        
        ```
        
        - **`machine`**: A module for interacting with hardware components like pins and I2C buses.
        - **`urequests`**: A library for making HTTP requests, used here to send data to ThingSpeak.
        - **`ujson`**: A module for working with JSON data, used to format the data being sent.
        - **`time`**: Provides time-related functions, used to control timing between sensor readings.
        - **`network`**: Handles network-related tasks, such as connecting to Wi-Fi.
    - **Constants and Configuration**
        
        ```python
        I2C_MODE = 0x01
        UART_MODE = 0x02
        DEV_ADDRESS = 0x22
        
        HPA = 0x01
        KPA = 0x02
        TEMP_C = 0x03
        TEMP_F = 0x04
        
        ```
        
    - Wi-Fi Connection Setup
        
        ```python
        ssid='MakerLab.vn' # Wi-Fi network name
        password='' # Wi-Fi password
        
        ```
        
        ```python
        sta_if=network.WLAN(network.STA_IF)
        sta_if.active(True)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())
        
        ```
        
        - This block connects the ESP32 to the specified Wi-Fi network. If not connected, it attempts to connect and waits until successful.
        
    - Setup function
        
        ```python
        def setup():
            i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
            sensor = DFRobot_Environmental_Sensor_I2C(i2c, DEV_ADDRESS)
            
            if not sensor.begin():
                print("Sensor initialization failed!!")
                return
        
            print("Sensor initialization success!!")
        
        ```
        
    - Data Collection and Uploading
        
        ```python
        while True:
            temperature_c = sensor.get_temperature(TEMP_C)
            temperature_f = sensor.get_temperature(TEMP_F)
            humidity = sensor.get_humidity()
            ultraviolet_intensity = sensor.get_ultraviolet_intensity()
            luminous_intensity = sensor.get_luminousintensity()
            atmospheric_pressure = sensor.get_atmosphere_pressure(HPA)
            elevation = sensor.get_elevation()
        
        ```
        
        ```python
        sensor_reading = {'field1':temperature_c, 'field2':humidity, 'field3':ultraviolet_intensity, 'field4':luminous_intensity, 'field5':atmospheric_pressure, 'field6': elevation}
        request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,json = sensor_reading, headers = HTTP_HEADERS )  
        request.close()
        time.sleep(1)
        
        ```
        
    

# 5. Web Platform

![User Interface Image 1](https://github.com/dngvmnh/Automatic_Weather_Station/raw/main/assets/demo_1.png)

To implement real-time weather and air quality updates on a web platform, the OpenWeatherMap API can be utilized effectively. Below is a guide on how to integrate this functionality using a JavaScript script within your web application.

## Setting Up Your HTML Elements

Before integrating the API, ensure your HTML file contains the necessary elements to display the weather data and air quality information. The script provided interacts with elements like `.date`, `.temp`, `.weather-content`, and several pollutant-specific elements. Here is an example structure:

```html
<div class="weather-widget">
    <div class="date"></div>
    <div class="temp"></div>
    <div class="temp-format"></div>
    <div class="weather-content"></div>
    <div class="aqi-value"></div>
    <div class="pollutants">
        <div class="co"></div>
        <div class="no"></div>
        <div class="no2"></div>
        <div class="o3"></div>
        <div class="so2"></div>
        <div class="pm2_5"></div>
        <div class="pm10"></div>
        <div class="nh3"></div>
    </div>
</div>

## Integrating the OpenWeatherMap API

To access the OpenWeatherMap API, you need an API key. Replace the placeholder in the script with your actual key. Also, specify the city or coordinates for which you want to fetch the weather and air quality data.

```
javascript
Copy code
const apiKey = 'YOUR_API_KEY';
const city = 'Ho Chi Minh City';
```
Alternatively, if you want to use geographical coordinates:

javascript
Copy code
const lat = 10.8231;  // Latitude for Ho Chi Minh City
const lon = 106.6297; // Longitude for Ho Chi Minh City
Weather Data Fetching
The script uses the weather endpoint to retrieve current weather data such as temperature, weather condition, and description. It then updates the respective HTML elements with this data.

javascript
Copy code
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
Air Quality Data Fetching
The air pollution endpoint provides data on the Air Quality Index (AQI) and concentrations of various pollutants. The script processes this information and updates the respective pollutant elements.

javascript
Copy code
function updateAirQuality() {
    fetch(airPollutionApiUrl)
        .then(response => response.json())
        .then(data => {
            const aqi = data.list[0].main.aqi;
            const components = data.list[0].components;

            aqiValueElement.innerHTML = `AQI Level: <span class="aqi-number">${aqi}</span>`;
            document.querySelector('.aqi-number').classList.add(`value-${aqi}`);

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
    Automatically Updating Data
The data updates every minute using the setInterval function. This ensures that your web application always displays the latest weather and air quality information.

javascript
Copy code
setInterval(updateDate, 60000);
setInterval(updateWeather, 60000);
setInterval(updateAirQuality, 60000);
    Error Handling
The script includes error handling to display fallback messages if the API requests fail. This ensures that the user interface remains informative even when the API is inaccessible.