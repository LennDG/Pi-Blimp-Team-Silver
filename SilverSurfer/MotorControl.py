#This is the file for the Motor Control class.
import Motor
from Vector import Vector
from math import pi

# parameters
    
# The factor by which a motor increases its acceleration for the same power going forwards 
FORWARD_FACTOR = 1  
    
# The factor by which the left motor is stronger than the right motor.
RELATIVE_FACTOR = 1


class MotorControl():
    
    
    
    def __init__(self):
        
        #Make all Motor objects
        self.left_motor = Motor.Motor(cw_pin = 4, ccw_pin = 24)
        self.right_motor = Motor.Motor(cw_pin = 10, ccw_pin = 11)
        self.vert_motor = Motor.VerticalMotor(cw_pin = 7, ccw_pin = 9) #Make sure that the PWM connector on the board is correct 
        
    
    # This method will make the zeppelin move forward or backward, depending on the direction.
    # direction    The anglein radians, the direction in which the zeppelin should move, makes with
    #              the forward direction. Directions to the left side of the zeppelin are positive.
    # acceleration The acceleration in percentage with which the zeppelin should propel itself forward.
    def move(self, angle, acceleration):
        
        # Reset motors
        self.left_off()
        self.right_off()
        
        # Normalize angle
        angle = angle%(2*pi)
        
        # Normalize acceleration
        acceleration = abs(acceleration)
        if acceleration > 100:
            acceleration = 100
        
        # Create a vector pointing in the direction the zeppelin should move, with norm the force.
        # The positive y-axis in the direction of the right motor, the positive x-axis
        # in the direction of the left motor..
        direction = Vector(0,acceleration).turn(angle - pi/4)     
        
        # Correct the vector for differences in motors and orientations. Depends on the value of the factor.
        # Always make sure the resizing results in smaller values, as values exceeding 100 can distort the
        # direction
        
        # Differences in motors
        direction.xcoord = direction.xcoord/RELATIVE_FACTOR
        
        # Differences in orientations
        if direction.ycoord > 0:
            direction.ycoord = direction.ycoord/FORWARD_FACTOR
        if direction.xcoord > 0:
            direction.xcoord = direction.xcoord/FORWARD_FACTOR
            
        self.left_motor.level = direction.xcoord
        self.right_motor.level = direction.ycoord
        
        self.left_motor.enable()
        self.right_motor.enable()
            
            
    def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
        self.left_off()
        self.right_off()
        
    def all_off(self):
        self.left_off()
        self.right_off()
        self.vert_off()
        
    def left_off(self): #This shuts the left engine down
        self.left_motor.disable()
    
    def right_off(self):#This shuts the right engine down
        self.right_motor.disable()
        
    def vert_off(self): #This shuts the vertical engine off
        self.vert_motor.disable()