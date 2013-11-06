#This is the file for the Motor Control class.
import Motor, time, DistanceSensor

class MotorControl():
    
    def __init__(self):
        
        self.left_motor = Motor.Motor(cw_pin = 4, ccw_pin = 24) #14 and 15 are next to 18 on BCM
        self.right_motor = Motor.Motor(cw_pin = 17, ccw_pin = 23)
        self.vert_motor = Motor.VerticalMotor(cw_pin = 7, ccw_pin = 9,enabler = 18)
        
    
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
        self.LeftMotor.disable()
        self.RightMotor.disable()