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
            ultraviolet = (outputVoltage - 0.99) * (15.0 - 0.0) / (2.9 - 0.99) + 0.0
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
        
        sensor_reading = {'field1':temperature_c, 'field2':humidity, 'field3':ultraviolet_intensity, 'field4':luminous_intensity, 'field5':atmospheric_pressure}
        print(sensor_reading) #in 2 giá trị gửi
        request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,json = sensor_reading, headers = HTTP_HEADERS )  
        request.close()
        time.sleep(1)


if __name__ == "__main__":
    setup()


