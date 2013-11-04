##This is the file for the Motor class
import RPi.GPIO as GPIO

class Motor(object):
    
    def __init__(self, cw_pin, ccw_pin, enabler):
        
        GPIO.setmode(GPIO.BCM)
        
        self.direction = 1
        
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        
        GPIO.setup(cw_pin, GPIO.OUT)
        GPIO.setup(ccw_pin, GPIO.OUT)
        
        #Reset the pins
        GPIO.output(cw_pin, 0)
        GPIO.output(ccw_pin, 0)
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value): #This sets the direction
        self._direction = value
    
    def enable(self): #This turns the motor on and sets the level and direction according to the attributes
        if self.direction >= 0:
            GPIO.output(self.ccw_pin, 0)
            GPIO.output(self.cw_pin, 1)
            
        else:
            GPIO.output(self.cw_pin, 0)
            GPIO.output(self.ccw_pin, 1)
    
    def disable(self): #This turns the motor off
        GPIO.output(self.cw_pin, 0)
        GPIO.output(self.ccw_pin, 0)
    
    
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