import time
import network
from machine import Pin, PWM
from mqtt import MQTTClient
from Motor import Motor #wrote a class for motor objects
import uasyncio as asyncio


# ---- MQTT THINGS ----
ssid = 'Tufts_Robot'
password = ''

#ssid = "ARRIS-9985"  # Network SSID
#password = "306865602614"  # Network key

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
        
def connect_mqtt(client):
    client.set_callback(callback)
    client.connect()
    client.subscribe(topic_sub.encode())
    print(f'Subscribed to {topic_sub}')

def callback(topic, msg):
    global isOn
     
    val = msg.decode()
    print((topic.decode(), val))
    
    if val == 'start':
        isOn = True
    elif val == 'stop':
        isOn = False
        rightMotor.stop()
    
    if isOn:
        if val[0] == 'R':
            rightMotor.turn(int(val[1:]))
        elif val[0] == 'F':
            rightMotor.goForward(int(val[1:])) # this will have to be rethought with two picos
        elif val[0] == 'B':
            rightMotor.goBackward(int(val[1:]))
        
async def mqtt_handler(client):
    while True:
        try:
            client.check_msg()
            await asyncio.sleep(0.01)
        except Exception as e:
            print('MQTT callback failed')
            connect_mqtt(client) 
            

# --- Defining pins and motor objects ----
motor1A = Pin('GPIO1', Pin.OUT)
motor1B = Pin('GPIO2', Pin.OUT)
motor1PWM = PWM(Pin('GPIO3', Pin.OUT))

rightMotor = Motor(motor1A, motor1B, motor1PWM, 'right')

connect_wifi()
client = MQTTClient('ME35_chris', mqtt_broker, port, keepalive=60)
connect_mqtt(client)
asyncio.run(mqtt_handler(client))
