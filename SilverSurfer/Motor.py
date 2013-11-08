#This is the file for the Motor class
import RPi.GPIO as GPIO

class Motor(object):
    
    def __init__(self, cw_pin, ccw_pin):
        
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
    
    def enable(self): #This turns the motor on and sets the direction according
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
    
    def __init__(self, cw_pin, ccw_pin):
        super(VerticalMotor, self).__init__(cw_pin, ccw_pin)
        self._level = 0.0
        self.PWM = 18 #Should not be changing since it's hardwired into the Pi!
        GPIO.setup(self.PWM, GPIO.OUT)
        self.enabler = GPIO.PWM(self.PWM,100)
        self.enabler.start(0.0)
        
    @property    
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        #Takes a value between -100.0 and 100.0
        if value >= 0:
            GPIO.output(self.ccw_pin, 0)
            GPIO.output(self.cw_pin, 1)
            
        else:
            GPIO.output(self.cw_pin, 0)
            GPIO.output(self.ccw_pin, 1)
            
        self.enabler.ChangeDutyCycle(abs(value)) #between 0.0 and 100.0
        self._level = value

    def disable(self):
        #Call the super class method
        super(VerticalMotor, self).disable()
        #Set the level to 0
        self.level = 0.0   