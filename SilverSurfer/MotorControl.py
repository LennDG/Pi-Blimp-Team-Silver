#This is the file for the Motor Control class.
import Motor, time, DistanceSensor

class MotorControl():
    
    def __init__(self, basis):
        
        self.left_motor = Motor.Motor(cw_pin = 4, ccw_pin = 24, enabler = 14) #14 and 15 are next to 18 on BCM
        self.right_motor = Motor.Motor(cw_pin = 17, ccw_pin = 23, enabler = 15)
        self.vert_motor = Motor.VerticalMotor(cw_pin = 7, ccw_pin = 9,enabler = 18)
        self.distance_sensor = DistanceSensor.DistanceSensor()
        
        self.basis = basis
    
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
    
    def turn(self, angle):
        
        self.left_motor.disable() #"reset" the motors
        self.right_motor.disable()
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        seconds = a*angle + b  #seconds is a function of angle
        
        #Calculate direction here (rechterhandregel yo)
        if angle >= 0:
            self.left_motor.direction = -1
            self.right_motor.direction = 1
        else:
            self.left_motor.direction = 1
            self.right_motor.direction = -1
        
        #motors start, turning begins.
        self.left_motor.enable()
        self.right_motor.enable() 
        
        #turning continues for the amount of secons calculated previously.
        time.sleep(seconds) #Seconden!
        
        #turning stops, motors disabled
        self.left_motor.disable()
        self.right_motor.disable()
        
    def stabilize(self, height):
        error =  self.distance_sensor.height - height
            
        b = 1 # b is a parameter that has yet to be defined through testing
            
        
        level = b*error*abs(error) + self.basis
        
        # Set the right direction for the vertical motor
        if level < 0:
            self.vert_motor.direction = -1
        else:
            self.vert_motor.direction = 1
            
            
    def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
        self.LeftMotor.disable()
        self.RightMotor.disable()