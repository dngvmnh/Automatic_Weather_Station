import machine
import urequests
import ujson as json
from machine import Pin,ADC
import network, time
import dht

dht_sensor = dht.DHT11(machine.Pin(33)) #kết nối cảm biến dht với chân 23 (D11 trên Shield)
soil = ADC(Pin(32)) # kết nối cảm biến với chân 34 (A1 trên shield)
soil.atten(ADC.ATTN_11DB)

#Thông tin tài khoản Thingspeak 
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '8RLXDPKT7Z4GSF9W' 

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

field1_request = 'https://api.thingspeak.com/channels/2588727/fields/1/last.json'

while True:
    dht_sensor.measure()
    temperature = dht_sensor.temperature() #đọc giá trị nhiệt độ
    humidity = dht_sensor.humidity() #đọc giá trị độ ẩm
    soil_value=soil.read()
    sensor_reading = {'field1':temperature, 'field2':humidity, 'field8':soil_value} #nối các giá trị thành 1 chuỗi để gửi
    print(sensor_reading) #in 2 giá trị gửi
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,json = sensor_reading, headers = HTTP_HEADERS )  
    request.close()
    
		#đọc giá trị từ field5 (nút nhấn) và bật-tắt đèn tương ứng
    
    time.sleep(5)