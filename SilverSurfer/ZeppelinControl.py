#This is the file for the ZeppelinControlfile
import MotorControl, time

class ZeppelinControl():
    
    def __init__(self):
        
        self.motor_control = MotorControl()
        self.current_height = 0
        self.goal_height = 0
    
    @property
    def current_heigth(self):
        return self.distance_sensor.height
    
    def go_to_height(self, height):
        self.goal_height = height
    
    def move(self, direction):
        self.motor_control.move(direction)
    
    def turn(self, direction):
        self.motor_control.turn(direction)
    
    def hor_stop(self): 
        #stops all horizontal movement (includes turning)
        self.motor_control.stop()
    
    def vert_stop(self):
        #stabilizes at current height
        self.stabilize(self.current_height)
    
    #This method calibrates the basis parameter by moving the zeppelin up and down untill it stabilises around a random height        
    def calibrate(self, increment):
        if self.isRising():
            self.motor_control.vert_motor.direction = -1
        else:
            self.motor_control.vert_motor.direction =  1
        self.subCalibrate(increment)
        self.motor_control.basis = self.motor_control.vert_motor.level
    
    def subCalibrate(self, increment, depth):
        if self.isRising():
            while self.isRising():
                self.motor_control.vert_motor.level -= self.motor_control.vert_motor.direction*increment
        else:
            while not self.isRising():
                self.motor_control.vert_motor.level += self.motor_control.vert_motor.direction*increment
        self.subCalibrate(increment/2, depth-1)
    
    #Returns if the zeppelin is gaining altitude.
    def isRising(self):
        height1 = self.distance_sensor.getHeight()
        time.sleep(0.5)
        height2 = self.distance_sensor.getHeight()
        return height2 - height1 > 0
            
    def stabilize(self, height):
        error =  self.distance_sensor.height - height
                
        b = 1 # b is a parameter that has yet to be defined through testing
                
            
        level = b*error*abs(error) + self.basis
            
        # Set the right direction for the vertical motor
        if level < 0:
            self.vert_motor.direction = -1
        else:
            self.vert_motor.direction = 1