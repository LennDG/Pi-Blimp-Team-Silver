#This is the file for the Motor Control class.
import Motor, time, DistanceSensor

class MotorControl():
    
    def __init__(self):
        
        self.left_motor = Motor.Motor(24,4) #This should pass the right GPIO as a variable, or something...
        self.right_motor = Motor.Motor(17,23)
        self.vert_motor = Motor.VerticalMotor(9,7)
        self.distance_sensor = DistanceSensor.DistanceSensor()
        
        self._speed = 0.0
        self._vertical = 0.0 #Base vertical level, eeeerrrrr, team talk necessary
    
    
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
        
    def stabilize(self, heigth):
        error = heigth - self.distance_sensor.heigth
        
        # Set the right direction for the vertical motor
        if error < 0:
            self.vert_motor.direction = -1
        else:
            self.vert_motor.direction = 1
            
        b = 1 # b is a parameter that has yet to be defined through testing
            
        level = b*error**2
        
    def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
        self.LeftMotor.disable()
        self.RightMotor.disable()