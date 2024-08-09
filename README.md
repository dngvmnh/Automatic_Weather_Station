## DEMO

![User Interface Image 1](https://github.com/dngvmnh/Automatic_Weather_Station/raw/main/assets/demo_1.png)

![User Interface Image 2](https://github.com/dngvmnh/Automatic_Weather_Station/blob/main/assets/demo_2.png)
## Project Description

### Overview

The Automatic Weather Station leverages the ESP32 microcontroller and the DFRobot Environmental Sensor to collect various environmental data, including temperature, humidity, ultraviolet intensity, luminous intensity, atmospheric pressure, and elevation. This data is transmitted to the ThingSpeak web server and displayed in real-time on a user-friendly website built with JavaScript.

### Station Features

- **Real-Time Data Visualization:** Weather data such as temperature, humidity, ultraviolet intensity, luminous intensity, atmospheric pressure, and elevation are graphically represented using ThingSpeak's HTML code. Additionally, air quality metrics, including CO, NO2, O3, and PM2.5 pollutant concentrations, are retrieved from OpenWeatherMap APIs and displayed.
- **Wireless Data Transmission:** The ESP32’s built-in Wi-Fi transmits collected data to the ThingSpeak platform using the ThingSpeak API and the provided Wi-Fi credentials. This data can be seamlessly displayed on a website built using templates from Google Sites or GitHub Pages.
- **Data Logging and Analysis:** The station logs collected data for historical analysis and trend monitoring. It also includes a feature for searching weather data in other cities. The station is designed for continuous operation with minimal power consumption.

### Setup

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

## Discussion

### Challenges and Limitations

- **Data Accuracy and Calibration:** while the DFRobot Environmental Sensor provides reliable readings, environmental sensors often require regular calibration to maintain accuracy over time. This process could be automated or streamlined in future versions of the project to ensure ongoing precision.
- **Power Consumption:** although the design focuses on minimal power consumption, continuous operation, especially with active Wi-Fi data transmission, can drain power sources quickly. Future iterations might explore the use of solar power or other renewable energy sources to extend the station's operational lifespan in remote areas.
- **Internet Dependency:** the project relies on a stable internet connection to transmit data to the ThingSpeak platform. In areas with poor connectivity, data transmission may be interrupted, leading to gaps in monitoring. Developing an offline data logging feature could address this limitation, allowing the station to store data locally until a connection is restored.
- **User Interface Design:** while the current web interface is functional, there is room for improvement in terms of aesthetics and user experience. Enhancements could include more interactive elements, customizable data views, or mobile-friendly design to cater to a broader audience.

### Future Enhancements

- **Advanced Analytics:** incorporating machine learning algorithms to analyze historical data could enable predictive modeling, offering forecasts or anomaly detection. This would significantly increase the utility of the weather station, especially in applications requiring proactive environmental management.
- **Integration with Other IoT Devices:** expanding the station's capability to interact with other IoT devices, such as smart home systems or agricultural sensors, could open up new use cases. For instance, the station could trigger irrigation systems based on soil moisture levels or alert users to poor air quality via a connected smart speaker.
- **Enhanced Data Security: a**s the station collects and transmits sensitive environmental data, implementing robust security measures, such as encryption and secure APIs, will be crucial in protecting data integrity and user privacy.

## Documentation
