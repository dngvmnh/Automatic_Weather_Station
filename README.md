## DEMO

![User Interface Image 1](https://prod-files-secure.s3.us-west-2.amazonaws.com/20ca33b6-85bf-42aa-b292-2895dee8f79f/f1282698-b611-48d7-9570-a57becd718a5/Untitled.png)

![User Interface Image 2](https://prod-files-secure.s3.us-west-2.amazonaws.com/20ca33b6-85bf-42aa-b292-2895dee8f79f/23781abb-79f9-42d2-ad41-d9e21f2732f1/Untitled.png)

## Project Description

### 1. Overview

The Automatic Weather Station leverages the ESP32 microcontroller and the DFRobot Environmental Sensor to collect various environmental data, including temperature, humidity, ultraviolet intensity, luminous intensity, atmospheric pressure, and elevation. This data is transmitted to the ThingSpeak web server and displayed in real-time on a user-friendly website built with JavaScript.

### 2. Station Features

- **Real-Time Data Visualization:** Weather data such as temperature, humidity, ultraviolet intensity, luminous intensity, atmospheric pressure, and elevation are graphically represented using ThingSpeak's HTML code. Additionally, air quality metrics, including CO, NO2, O3, and PM2.5 pollutant concentrations, are retrieved from OpenWeatherMap APIs and displayed.
- **Wireless Data Transmission:** The ESP32’s built-in Wi-Fi transmits collected data to the ThingSpeak platform using the ThingSpeak API and the provided Wi-Fi credentials. This data can be seamlessly displayed on a website built using templates from Google Sites or GitHub Pages.
- **Data Logging and Analysis:** The station logs collected data for historical analysis and trend monitoring. It also includes a feature for searching weather data in other cities. The station is designed for continuous operation with minimal power consumption.

### 3. Setup

- Install the Arduino IDE or Thonny IDE.
- Install the required libraries for the ESP32 and DFRobot Sensor.
- Upload the provided code to the ESP32.
- Connect the DFRobot Environmental Sensor to the ESP32 following the wiring diagram provided in the documentation.
- Power the ESP32 using a micro USB cable or a battery, and connect it to an adapter once coding is complete.
- The weather station will automatically begin collecting and transmitting data, which can be accessed through the web interface via browser.

## Implementation

### Hardware

- **ESP32 Microcontroller:** Manages data collection, signal processing, and transmission.
- **DFRobot Environmental Sensor:** Measures various environmental parameters.
- **ThingSpeak Platform:** Facilitates data logging and cloud storage.
- **Web Server:** Can be hosted using Google Sites or GitHub Pages to display the fetched data.

### Software

- Set up a local or remote server to host the web interface using Google Sites or GitHub Pages.
- Upload the provided HTML, CSS, and JavaScript files to the server.
- Configure the ESP32 to transmit data to the server’s IP address.

### Code Structure

- **MicroPython:** Used for collecting data from the DFRobot Environmental Sensor and communicating with ThingSpeak.
- **HTML:** Provides the main structure of the web page, organized into sections for location, current weather, air quality, and footer.
- **CSS:** Styles the interface, including layout, animations, and responsiveness.
- **JavaScript:** Manages data fetching from APIs, updates weather and air quality information, and handles user interactions.

## Results and Discussion

## Documentation
