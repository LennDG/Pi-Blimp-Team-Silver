"""
This class simulates a motor object by granting acces to a level
that can be modified.
"""

class MotorSimulator(object):
    
    def __init__(self):
        
        self._level = 5.0
        
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value): #This sets the level of the motor
        if value > 100.0:
            value = 100.0
        elif value < -100.0:
            value = -100.0
        self._level = value