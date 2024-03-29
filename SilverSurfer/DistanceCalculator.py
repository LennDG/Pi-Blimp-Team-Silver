import time, random
import threading

class DistanceCalculator(object):
    
    C_W = 1 # Think this is about right.
    MASS = 0.3 # Determine this 
    SURFACE_AREA = 2 # Determine this
    AIR_DENSITY = 1000 # I think this is alright
    GRAVITY = 9.81
    MOTOR_POWER = 2 # test this #verschil in gewicht
    
    def __init__(self, error_level, data_amount):
        
        self.navigator = 0
        
        self.error_level = error_level   # standard deviation in centimeters
        self.data_amount = data_amount   #amount of data we take the average height from
        self.interval = 0.06*self.data_amount 
        
        self.height = 0.00
        self.speed = 0 # positive for up, negative for downwards.
        self.acceleration = 0
        
    
    @property    
    def motor_level(self):
        return self.navigator.motor_control.vert_motor.level

    def calculate_height(self):
#         self.acceleration = (self.motor_level*DistanceCalculator.MOTOR_POWER - DistanceCalculator.SURFACE_AREA*DistanceCalculator.AIR_DENSITY*DistanceCalculator.C_W*self.speed**2/10)/DistanceCalculator.MASS - DistanceCalculator.GRAVITY
#         new_speed = self.speed + self.acceleration*self.interval
#         new_height = self.height + (new_speed + self.speed)/2*self.interval # The speed has increased linearly over the interval.
#         new_height = new_height + self.error_level*random.gauss(1, 1)
        new_height = self.navigator.goal_height + random.gauss(0, self.error_level)
        if new_height < 0:
            new_height = 0
        self.height = new_height
        
        