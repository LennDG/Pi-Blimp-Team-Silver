#This is the file for the Motor Control class.
import Motor, time, DistanceSensor

class MotorControl():
    
    def __init__(self):
        
        #Make all Motor objects
        self.left_motor = Motor.Motor(cw_pin = 4, ccw_pin = 24)
        self.right_motor = Motor.Motor(cw_pin = 17, ccw_pin = 23)
        self.vert_motor = Motor.VerticalMotor(cw_pin = 7, ccw_pin = 9) #Make sure that the PWM connector on the board is correct 
        
    
    # This method will make the zeppelin move forward or backward, depending on the direction.
    # direction    1 to move forward
    #              -1 to move backward
    def move(self, direction):
        self.left_motor.disable()
        self.right_motor.disable()
        
        self.left_motor.direction = direction
        self.right_motor.direction = direction
        
        self.left_motor.enable()
        self.right_motor.enable()
    
    
    def turn(self, direction):
        
        self.left_motor.disable() #"reset" the motors
        self.right_motor.disable()
        
        self.left_motor.direction = -direction
        self.right_motor.direction = direction
       
        #motors start, turning begins.
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