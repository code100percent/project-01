from machine import Pin
import network
import socket
from time import sleep
from gpio_lcd import GpioLcd

wifi_ssid = 'Airtel_harb_0675'
wifi_pass = 'air11173'
lcd = GpioLcd(rs_pin=Pin(0),
              enable_pin=Pin(1),
              d4_pin=Pin(2),
              d5_pin=Pin(3),
              d6_pin=Pin(4),
              d7_pin=Pin(5),
              num_lines=2, num_columns=16)

statusLed = Pin(13,Pin.OUT)
statusLed.value(1)
ip_confirm_led = Pin('LED',Pin.OUT)
ip_confirm_led.value(0)
#motor pins
mRight1 = Pin(16,Pin.OUT)
mRight2 = Pin(17,Pin.OUT)
mLeft1 = Pin(14,Pin.OUT)
mLeft2 = Pin(15,Pin.OUT)
mRight1.value(0)
mRight2.value(0)
mLeft1.value(0)
mLeft2.value(0)
def run_motor(cmd):
    if cmd.lower() == 'forward':
        mRight1.value(1)
        mRight2.value(0)
        mLeft1.value(1)
        mLeft2.value(0)
    if cmd.lower() == 'backward':
        mRight1.value(0)
        mRight2.value(1)
        mLeft1.value(0)
        mLeft2.value(1)
    if cmd.lower() == 'left':
        mRight1.value(1)
        mRight2.value(0)
        mLeft1.value(0)
        mLeft2.value(1)
    if cmd.lower() == 'right':
        mRight1.value(0)
        mRight2.value(1)
        mLeft1.value(1)
        mLeft2.value(0)
        
    if cmd.lower() == 'stop':
        mRight1.value(0)
        mRight2.value(0)
        mLeft1.value(0)
        mLeft2.value(0)
        
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
lcd.f_write(f'connecting to   {wifi_ssid}')
wifi.connect(wifi_ssid,wifi_pass)
sleep(2)
cnt=1

while wifi.isconnected() == False:
    print('waiting to connect...',cnt)
    lcd.f_write('waiting to connect...')
    lcd.move_to(0,1)
    lcd.putstr(str(cnt))
    sleep(1)
    cnt +=1
for i in range(4):
    statusLed.value(0)
    sleep(0.4)
    statusLed.value(1)
    sleep(0.4)
statusLed.value(0)
CarServerIP = wifi.ifconfig()[0]
if CarServerIP == '192.168.1.7':
    ip_confirm_led.value(1)
CarServerPort = 2222
BufferSize = 1024
print('wifi connected successfully')
lcd.f_write('wifi IP :')
lcd.move_to(0,1)
lcd.putstr(CarServerIP)
print(CarServerIP)
UDPServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDPServer.bind((CarServerIP,CarServerPort))
while True:
    print('waiting for any message....')
    statusLed.value(1)
    message,address=UDPServer.recvfrom(BufferSize)
    statusLed.value(0)
    messageDecoded=message.decode('utf-8')
    print(messageDecoded)
    run_motor(messageDecoded)
    







    