import time
import network
from machine import Pin, PWM
from mqtt import MQTTClient
from Motor import Motor #wrote a class for motor objects
import uasyncio as asyncio


# ---- MQTT THINGS ----
ssid = 'Tufts_Robot'
password = ''

mqtt_broker = 'broker.hivemq.com'
port = 1883
topic_sub = 'ME35-24/longshark'

isOn = False

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
        
def callback(topic, msg):
    global isOn
    
    val = msg.decode()
    print((topic.decode(), val))
    
    if val == 'start':
        isOn = True
    elif val == 'stop':
        isOn = False
        leftMotor.stop()
    
    if isOn:
    
        if val[0] == 'L':
            leftMotor.turn(int(val[1:]))
        elif val[0] == 'F':
            leftMotor.goForward(int(val[1:]))
        elif val[0] == 'B':
            leftMotor.goBackward(int(val[1:]))

        
async def mqtt_handler(client):
    while True:
        client.check_msg()
        await asyncio.sleep(0.01)


# --- Defining pins and motor objects ----
motor1A = Pin('GPIO1', Pin.OUT)
motor1B = Pin('GPIO2', Pin.OUT)
motor1PWM = PWM(Pin('GPIO3', Pin.OUT))
leftMotor = Motor(motor1A, motor1B, motor1PWM, 'left')

connect_wifi()
client = MQTTClient('ME35_chris', mqtt_broker, port, keepalive=60)
client.set_callback(callback)
client.connect()
client.subscribe(topic_sub.encode())
print(f'Subscribed to {topic_sub}')
asyncio.run(mqtt_handler(client))
