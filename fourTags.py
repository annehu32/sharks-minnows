# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

# Code samples from OPEN MV examples: mqttt_pub and find_apriltags_3d_pose1
# Second try with Apriltag joystick:
# This time, four tags: forward, backward, left right
# distance from tag will indicate a magnitude


# Librarys for mqtt
import time
import network
from mqtt import MQTTClient

# Libraries for aprilTags
import sensor
import time
import math

# ----- MQTT SETUP -----
SSID = "Tufts_Robot"  # Network SSID
KEY = ""  # Network key

# Init wlan module and connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

while not wlan.isconnected():
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

client = MQTTClient('ME35_anneCamera', 'broker.hivemq.com', port=1883)
client.connect()

# ---- CAMERA SETUP -----
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# ------ APRILTAG SETUP -----
# Using tags 0-3 from Tag Family tag36h11
tagID = ['F','B','L','R']


# ----- HELPER FUNCTIONS -----
# Takes z-translational value, returns a duty cycle
def zPercent(trans):
    max_trans = 1.95 # the closest translational x-value read
    return int(65535 * (max_trans/ abs(trans)))


# --------- MAIN CODE ---------------
while True:
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():  # No arguments for now
        img.draw_rectangle(tag.rect(), color=(255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))

        z = tag.z_translation()
        tagNum = tag.id()

        print("name: " + str(tagNum) + ", z: "+str(z)+ ", z percent: "+ str(zPercent(z)))

        # Publishes value over MQTT
        if tagNum < 4: # filters out any mis-reads to prevent index errors
            client.publish("ME35-24/longshark", tagID[tagNum]+str(zPercent(z)))
            time.sleep(0.01)


    print(clock.fps())

