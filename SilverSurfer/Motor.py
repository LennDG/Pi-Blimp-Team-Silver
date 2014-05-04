#This is the file for the Motor class
import RPi.GPIO as GPIO
import threading, time

class Motor(object):
    
    def __init__(self, cw_pin, ccw_pin, motor_place):
        self._level = 0.0
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        self.motor_place = motor_place
        
        self.motor_thread = None

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        if self.motor_place == 'left':
            self.motor_thread.left_level = value
        elif self.motor_place == 'right':
            self.motor_thread.right_level = value
        
        

class MotorThread(threading.Thread, object):
    
    def __init__(self, left_cw_pin, left_ccw_pin, right_cw_pin, right_ccw_pin, frequency):
        
        threading.Thread.__init__(self)
        
        GPIO.setmode(GPIO.BCM)
        
        self._left_level = 0.0
        self._right_level = 0.0
        
        self.frequency = frequency
        
        self.left_cw_pin = left_cw_pin
        self.left_ccw_pin = left_ccw_pin

        self.right_cw_pin =  right_cw_pin
        self.right_ccw_pin =  right_ccw_pin

        
        GPIO.setup(left_cw_pin, GPIO.OUT)
        GPIO.setup(left_ccw_pin, GPIO.OUT)
        
        GPIO.setup(right_cw_pin, GPIO.OUT)
        GPIO.setup(right_ccw_pin, GPIO.OUT)
        
        #Reset the pins
        GPIO.output(left_cw_pin, 0)
        GPIO.output(left_ccw_pin, 0)
        
        GPIO.output(right_cw_pin, 0)
        GPIO.output(right_ccw_pin, 0)
        
        
    @property
    def left_level(self):
        return self._left_level
    
    @property
    def right_level(self):
        return self._right_level
    
    @left_level.setter
    def left_level(self, value): #This sets the level of the motor
        if value > 100:
            value = 100
        elif value < -100:
            value = -100
        self._left_level = value
        
    @right_level.setter
    def right_level(self, value): #This sets the level of the motor
        if value > 100:
            value = 100
        elif value < -100:
            value = -100
        self._right_level = value
        
    def run(self):
        while True:
            right_on_time = abs(self.right_level)/(100.*self.frequency)
            left_on_time = abs(self.left_level)/(100.*self.frequency)
            
            if left_on_time > right_on_time:
                if self.left_level > 0.0: GPIO.output(self.left_cw_pin, 1)
                else: GPIO.output(self.left_ccw_pin, 1)
                if self.right_level > 0.0: GPIO.output(self.right_cw_pin, 1)
                else: GPIO.output(self.right_ccw_pin, 1)
                time.sleep(right_on_time)
                GPIO.output(self.right_cw_pin, 0)
                GPIO.output(self.right_ccw_pin, 0)
                time.sleep(left_on_time - right_on_time)
                GPIO.output(self.left_cw_pin, 0)
                GPIO.output(self.left_ccw_pin, 0)
                
                time.sleep(abs(1./self.frequency - left_on_time))
                
            elif right_on_time > left_on_time:
                if self.left_level > 0.0: GPIO.output(self.left_cw_pin, 1)
                else: GPIO.output(self.left_ccw_pin, 1)
                if self.right_level > 0.0: GPIO.output(self.right_cw_pin, 1)
                else: GPIO.output(self.right_ccw_pin, 1)
                time.sleep(left_on_time)
                GPIO.output(self.left_cw_pin, 0)
                GPIO.output(self.left_ccw_pin, 0)
                time.sleep(right_on_time - left_on_time)
                GPIO.output(self.right_cw_pin, 0)
                GPIO.output(self.right_ccw_pin, 0)    
                
                time.sleep(abs(1./self.frequency - right_on_time))          
    
class VerticalMotor(object):
    
    def __init__(self, cw_pin, ccw_pin):
        self._level = 0.0
        
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        
        GPIO.setup(cw_pin, GPIO.OUT)
        GPIO.setup(ccw_pin, GPIO.OUT)
        
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
