#This is the file for the ZeppelinControlfile
import MotorControl

class ZeppelinControl():
    
    def __init__(self):
        
        self.motor_control = MotorControl()
        self.current_heigth = 0
    
    @property
    def current_heigth(self):
        return self.distance_sensor.height
    
    
    