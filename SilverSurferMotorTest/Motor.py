'''
Created on 4-nov.-2013

@author: Lily
'''

##This is the file for the Motor class
import RPi.GPIO as GPIO

class Motor():
    
    def __init__(self, cw_pin, ccw_pin, enabler):
        
        GPIO.setmode(GPIO.BCM)
        
        self._direction = 1
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        self.enabler = enabler
        
        GPIO.setup(cw_pin, GPIO.OUT)
        GPIO.setup(ccw_pin, GPIO.OUT)
        GPIO.setup(enabler, GPIO.OUT)
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value): #This sets the direction
        self._direction = value
        if value == 1:
            GPIO.output(self.ccw_pin, 0)
            GPIO.output(self.cw_pin, 1)
            
        else:
            GPIO.output(self.cw_pin, 0)
            GPIO.output(self.ccw_pin, 1)
    
    def enable(self): #This turns the motor on and sets the level and direction according to the attributes
        GPIO.output(self.enabler, 1)
    
    def disable(self): #This turns the motor off
        GPIO.output(self.enabler, 0)
    
    
class VerticalMotor(Motor):
    
    def __init__(self, cw_pin, ccw_pin, enabler):
        super(VerticalMotor, self).__init__(self, cw_pin, ccw_pin)
        self._level = 0.0
        self.enabler = GPIO.PWM(enabler,10)
        enabler.start(0.0)
        
        
    @property    
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        self.enabler.ChangeDutyCycle(value) #between 0.0 and 100.0
        self._level = value

    def disable(self):
        #Set the level to 0
        self.level = 0.0   