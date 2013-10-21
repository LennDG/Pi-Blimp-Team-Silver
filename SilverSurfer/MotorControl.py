#This is the file for the Motor Control class.
import Motor, time

class MotorControl():
    
    def __init__(self):
        
        self.left_motor = Motor() #This should pass the right GPIO as a variable, or something...
        self.right_motor = Motor()
        self.vert_motor = Motor()
        
        self._speed = 0.0
        self._vertical = 0.0 #Base vertical level, eeeerrrrr, team talk necessary
        
        
    #REASONING: Easier to let it run without babysitting the function!
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        
        self.LeftMotor.disable() #"reset" the motor
        self.RightMotor.disable()
        
        self.LeftMotor.level = value #Not really sure how to represent the level yet.
        self.RightMotor.level = value
        
        if value >= 0:
            self.LeftMotor.direction = 1
            self.RightMotor.direction = 1
        else:
            self.LeftMotor.direction = -1
            self.RightMotor.direction = -1
            
        self.LeftMotor.enable()
        self.RightMotor.enable()
        
        
    
    def turn(self, angle):
        
        self.LeftMotor.disable() #"reset" the motors
        self.RightMotor.disable()
        
        #Calculate values for engines and amount of time necessary here...
        value = angle
        seconds = angle*2 #Hurr Durr
        
        self.LeftMotor.level = value 
        self.RightMotor.level = value
        
        #Calculate direction here (rechterhandregel yo)
        if angle >= 0:
            self.LeftMotor.direction = -1
            self.RightMotor.direction = 1
        else:
            self.LeftMotor.direction = 1
            self.RightMotor.direction = -1
        
        self.LeftMotor.enable()
        self.RightMotor.enable()
        
        time.sleep(seconds) #Seconden!
        
        self.LeftMotor.disable()
        self.RightMotor.disable()
        
    def lift(self, amount):#Learning algorithm for defining parameters of stabilize? Probably the only way to reliably stabilize
        pass
    
    def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
        self.LeftMotor.disable()
        self.RightMotor.disable()