import time, random
import threading

class DistanceCalculator(threading.Thread, object):
    
    C_W = 1 # Think this is about right.
    MASS = 0.3 # Determine this
    SURFACE_AREA = 2 # Determine this
    AIR_DENSITY = 1000 # I think this is alright
    GRAVITY = 9.81
    MOTOR_POWER = 2 # test this
    
    def __init__(self, error_level, data_amount):
        
        threading.Thread.__init__(self)
        
        self.navigator = 0
        
        self.error_level = error_level   #between 0 and 5
        self.data_amount = data_amount   #amount of data we take the average height from
        self.interval = 0.06*self.data_amount 
        
        self.height = 0.00
        self.speed = 0 # positive for up, negative for downwards.
        self.acceleration = 0
        
    
    @property    
    def motor_level(self):
        return self.navigator.motor_control.vert_motor.level
 
    def run(self):
        while True:
            self.calculate_height() #Continually calculate the height
            time.sleep(self.interval)

    def calculate_height(self):
        self.acceleration = (self.motor_level*DistanceCalculator.MOTOR_POWER - DistanceCalculator.SURFACE_AREA*DistanceCalculator.AIR_DENSITY*DistanceCalculator.C_W*self.speed**2/2)/DistanceCalculator.MASS - DistanceCalculator.GRAVITY
        new_speed = self.speed + self.acceleration*self.interval
        new_height = self.height + (new_speed + self.speed)/2*self.interval # The speed has increased linearly over the interval.
        new_height = new_height + self.error_level*random.gauss(1, 1)
        if new_height < 0:
            new_height = 0
        self.height = new_height
        print self.height
        
        