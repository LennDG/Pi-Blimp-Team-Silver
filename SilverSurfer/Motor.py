#This is the file for the Motor class
import RPi.GPIO as GPIO
import threading, time

class Motor(threading.thread, object):
    
    def __init__(self, cw_pin, ccw_pin, frequency):
        
        threading.Thread.__init__(self)
        
        GPIO.setmode(GPIO.BCM)
        
        self.level = 0
        
        self.frequency = frequency
        
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin

        
        GPIO.setup(cw_pin, GPIO.OUT)
        GPIO.setup(ccw_pin, GPIO.OUT)
        
        #Reset the pins
        GPIO.output(cw_pin, 0)
        GPIO.output(ccw_pin, 0)
        
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value): #This sets the level of the motor
        if value > 100.0:
            value = 100.0
        elif value < -100.0:
            value = -100.0
        self._level = value
        
    def run(self):
        while True:
            if self.level > 0.0:
                on_time = self.level*1./self.frequency
                GPIO.output(self.cw_pin, 1)
                time.sleep(on_time)
                GPIO.output(self.cw_pin, 0)
                time.sleep(1/self.frequency - on_time)
                continue
            elif self.level < 0.0:
                on_time = self.level*1/self.frequency
                GPIO.output(self.ccw_pin, 1)
                time.sleep(on_time)
                GPIO.output(self.ccw_pin, 0)
                time.sleep(1./self.frequency - on_time)
                continue
            elif self.level == 0.0:
                GPIO.output(self.cw_pin, 0)
                GPIO.output(self.ccw_pin, 0)
        pass
        
    
class VerticalMotor(object):
    
    def __init__(self, cw_pin, ccw_pin):
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
        if value > 0:
            GPIO.output(self.ccw_pin, 0)
            GPIO.output(self.cw_pin, 1)
            
        elif value < 0:
            GPIO.output(self.cw_pin, 0)
            GPIO.output(self.ccw_pin, 1)
            
        elif value == 0.0:
            GPIO.output(self.cw_pin, 0)
            GPIO.output(self.ccw_pin, 0)
            
        self.enabler.ChangeDutyCycle(abs(value)) #between 0.0 and 100.0
        self._level = value

    def disable(self):
        #Set the level to 0
        self.level = 0.0   