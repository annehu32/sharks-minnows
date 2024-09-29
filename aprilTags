# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

# Code samples from OPEN MV examples: mqttt_pub and find_apriltags_3d_pose1


# Librarys for mqtt
import time
import network
from mqtt import MQTTClient

# Libraries for aprilTags
import sensor
import time
import math

# ----- MQTT Setup -----
SSID = "Tufts_Robot"  # Network SSID
KEY = ""  # Network key

# Init wlan module and connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

# ---- Camera Setup -----
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

while not wlan.isconnected():
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

client = MQTTClient('ME35_chris_pub', 'broker.hivemq.com', port=1883)
client.connect()

# ----- HELPER FUNCTIONS -----
def xPercent(trans):
    # ranging from 6 on the right to -6 on the left
    # want to convert from this range to a percentage of 25-100 percent
    max_trans = 6.5 # the largest translational x-value read
    return 100 * (trans/ (max_trans))**2

def yPercent(trans):
    max_trans = 6.8 # the largest translational x-value read
    return 100 * (trans/ (max_trans))**2

# --------- MAIN CODE ---------------
while True:
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():  # No arguments for now
        img.draw_rectangle(tag.rect(), color=(255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))

        x = tag.x_translation() # -x is right, +x is left
        y = tag.y_translation()

        # Reading AprilTag x-data for steering
        print("x: "+str(x)+", y: "+str(y))
        if x > 0:
            print("---- going left ----")
            client.publish("ME35-24/longshark", "L"+str(xPercent(x)))
        elif x< 0:
            print("--- going right ---")
            client.publish("ME35-24/longshark", "R"+str(xPercent(x)))


#        # Reading AprilTag y-data for speed
#        if y > 0:
#            print("--- FULL SPEED AHEAD!!! ----")
#            client.publish("ME35-24/longshark", "F"+str(yPercent(y)))
#        elif y < 0:
#            print("---- Speed: SPEEDY RETREAT!!! ----")
#            client.publish("ME35-24/longshark", "B"+str(yPercent(y)))

    print(clock.fps())

#while True:
#    client.publish("ME35-24/shark", "Hello World!")
#    time.sleep_ms(1000)
