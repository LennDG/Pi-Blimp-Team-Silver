##This is the file for the Motor class

class Motor():
    
    def __init__(self): #Does this need GPIO pin?
        
        self._level = 0.0
        self._direction = 1
    
    @property
    def level(self): #This returns the level
        return self._level
    
    @level.setter
    def level(self, value): #This sets the level
        self._level = value
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value): #This sets the direction
        self._direction = value
    
    def enable(self): #This turns the motor on and sets the level and direction according to the attributes
        #Set pin High
        pass
    
    def disable(self): #This turns the motor off
        #Set pin Low
        pass