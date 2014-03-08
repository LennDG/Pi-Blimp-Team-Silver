#This is the file for the Motor Control class.
from Vector import Vector
from math import pi


class MotorControl():
    
    FORWARD_SCALING = 1
    
    def __init__(self, left_motor, right_motor, vert_motor):
        
        # Assign all the motor objects. They should already be running.
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.vert_motor = vert_motor
        
    
    # This method will make the zeppelin move forward or backward, depending on the direction.
    # direction    The anglein radians, the direction in which the zeppelin should move, makes with
    #              the forward direction. Directions to the left side of the zeppelin are positive.
    # acceleration The acceleration in percentage with which the zeppelin should propel itself forward.
    def move(self, angle, acceleration):
        
        # Normalize angle
        angle = angle%(2*pi)
        
        # Normalize acceleration
        acceleration = abs(acceleration)
        if acceleration > 100:
            acceleration = 100
        
        # Create a vector pointing in the direction the zeppelin should move, with norm the acceleration.
        # The positive y-axis in the direction of the right motor, the positive x-axis
        # in the direction of the left motor..
        direction = Vector(0, acceleration).turn(angle - pi/4)     
        
        # Correct the vector for differences in orientations. Depends on the value of the factor.
        # Always make sure the resizing results in smaller values, as values exceeding 100 can distort the
        # direction
        
        
        # Differences in orientations
        if direction.ycoord > 0:
            direction.ycoord = direction.ycoord*MotorControl.FORWARD_SCALING
        if direction.xcoord > 0:
            direction.xcoord = direction.xcoord*MotorControl.FORWARD_SCALING
            
        self.left_motor.level = direction.xcoord
        self.right_motor.level = direction.ycoord
            
            
    def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
        self.left_off()
        self.right_off()
        
    def all_off(self):
        self.left_off()
        self.right_off()
        self.vert_off()
        
    def left_off(self): #This shuts the left engine down
        self.left_motor.level = 0
    
    def right_off(self):#This shuts the right engine down
        self.right_motor.level = 0
        
    def vert_off(self): #This shuts the vertical engine off
        self.vert_motor.level = 0