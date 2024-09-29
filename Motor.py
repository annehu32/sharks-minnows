import time
import network
from machine import Pin, PWM

class Motor():
    
    #Constants to be fiddled with
    pwmMin = 25
    pwmMax = 255

    # Initializer takes pins for the neopixel and buzzer
    def __init__(self, pin1, pin2, pwm, name):
        self.forward = pin1 #Should be PWM
        self.back = pin2 #Should be PWM
        self.pwm = pwm
        self.name = name
        print('motor instantiated, name: '+self.name)
        
        self.pwm.freq(1000)
    
    def goForward(self, val):
        print(self.name + ' moving forward')
        self.back.off()
        time.sleep(0.01)
        self.forward.on()
        self.pwm.duty_u16(int(val*65535/100))
    
    def goBackward(self, val):
        print(self.name + ' moving backward')
        self.forward.off()
        time.sleep(0.01)
        self.back.on()
        self.pwm.duty_u16(int(val*65535/100)) # where val is a %

    def stop(self):
        print(self.name + ' stopping ')
        self.forward.off()
        self.back.off()
    
    def test(self):
        for i in range(25,101):
            self.goForward(i)
            print(i)
            time.sleep(0.05)
        for i in range(25, 101):
            self.goBackward(i)
            time.sleep(0.05)
        self.stop()
