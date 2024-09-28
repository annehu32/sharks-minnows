import time
import network
from machine import Pin, PWM

class Motor():

    # Initializer takes pins for the neopixel and buzzer
    def __init__(self, pin1, pin2, name):
        self.forward = pin1
        self.back = pin2
        self.name = name
        print('motor instantiated, name: '+self.name)
    
    def goForward(self):
        print(self.name + ' motor moving forward')
        self.back.off()
        time.sleep(0.01)
        self.forward.on()
    
    def goBackward(self):
        print(self.name + ' motor moving backward')
        self.forward.off()
        time.sleep(0.01)
        self.back.on()
        
    def stop(self):
        print(self.name + ' motor stopping ')
        self.forward.off()
        self.back.off()
    
    def test(self):
        self.goForward()
        time.sleep(1)
        self.goBackward()
        time.sleep(1)
        self.stop()
