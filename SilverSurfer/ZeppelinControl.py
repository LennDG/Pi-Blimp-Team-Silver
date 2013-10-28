#This is the file for the ZeppelinControlfile
import MotorControl

class ZeppelinControl():
    
    def __init__(self):
        
        self.motor_control = MotorControl()
        self.current_heigth = 0
    
    @property
    def current_heigth(self):
        return self.distance_sensor.height
    
    def goToHeight(self, hoogte):
        pass
    
    def move(self, afstand):
        pass
    
    def turn(self, hoek):
        pass
    
    def stop(self): 
        pass