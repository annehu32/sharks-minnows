import time
import network
from machine import Pin, PWM
from mqtt import MQTTClient
from Motor import Motor #wrote a class for motor objects
import uasyncio as asyncio


# ---- MQTT THINGS ----

mqtt_broker = 'broker.hivemq.com'
port = 1883
topic_sub = 'ME35-24/longshark'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
        
def callback(topic, msg):
    print((topic.decode(), msg.decode()))
    if msg.decode() == 'right':
        rightMotor.goForward()
        
    elif msg.decode() == 'left':
        leftMotor.goForward()
    
    elif msg.decode() == 'forward':
        rightMotor.goForward()
        leftMotor.goForward()
    
    elif msg.decode() == 'backward':
        rightMotor.goBackward()
        leftMotor.goBackward()
    
    elif msg.decode() == 'stop':
        rightMotor.stop()
        leftMotor.stop()
        
async def mqtt_handler(client):
    while True:
        client.check_msg()
        await asyncio.sleep(0.1)




# --- Defining pins and motor objects ----
motor1A = Pin('GPIO1', Pin.OUT)
motor1B = Pin('GPIO2', Pin.OUT)
motor2A = Pin('GPIO3', Pin.OUT)
motor2B = Pin('GPIO4', Pin.OUT)

leftMotor = Motor(motor1A, motor1B,'left')
rightMotor = Motor(motor2A, motor2B, 'right')

leftMotor.test()
rightMotor.test()

connect_wifi()
client = MQTTClient('ME35_chris', mqtt_broker, port, keepalive=60)
client.set_callback(callback)
client.connect()
client.subscribe(topic_sub.encode())
print(f'Subscribed to {topic_sub}')
asyncio.run(mqtt_handler(client))
