##This is the file for the Motor class



class Motor():
    
    def __init__(self, cw_pin, ccw_pin, enabler): #Does this need GPIO pin?
        
        self._direction = 1
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        self.enabler = enabler
        
        #GPIO.setup(cw_pin, GPIO.OUT)
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value): #This sets the direction
        self._direction = value
        # Hier moeten de pinnekes nog geset worden.
        if value == 1:
            pass
            #GPIO.output(cw_pin, 1)
            #GPIO.output(ccw_pin, 0)
        else:
            #omgekeerd
            pass
        
    
    def enable(self): #This turns the motor on and sets the level and direction according to the attributes
        #Set pin High
        pass
    
    def disable(self): #This turns the motor off
        #Set pin Low
        pass
    
    
class VerticalMotor(Motor):
    
    def __init__(self, cw_pin, ccw_pin, enabler):
        super(VerticalMotor, self).__init__(self, cw_pin, ccw_pin, enabler)
        self._level = 0.0
        #Set right GPIO pins
        #self.p = GPIO.PWM(18,10)
        
        
    @property    
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        #Calculate dc and frequency
        #p.start(level) between 0.0 and 100.0
        pass

    def disable(self):
        #Set the level to 0
        self.level = 0.0   