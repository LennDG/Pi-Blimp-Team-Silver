from math import sqrt, asin, sin, cos, pi
from numbers import Number


class Vector(object):
    
    
    def __init__(self, xcoord, ycoord):
        self.xcoord = xcoord
        self.ycoord = ycoord
    
    #hoek van -pi...pi
    @property    
    def angle(self):
        
        angle = asin(self.ycoord/(self.norm + 0.0001))
        if self.xcoord >= 0:
            pass
        elif self.ycoord >= 0:
            angle = pi - angle 
        else:
            angle = -pi - angle
        return angle
             
    
    #Retrieves the length of the vector    
    @property    
    def norm(self):
        return sqrt(self.xcoord**2 + self.ycoord**2)
    
    def inner_product(self, other):
        X = self.xcoord*other.xcoord
        Y = self.ycoord*other.ycoord
        return X + Y
    
    def turn(self, angle):
        norm = self.norm
        angle = self.angle + angle
        xcoord = norm*cos(angle)
        ycoord = norm*sin(angle)
        return Vector(xcoord, ycoord)
        
    
    # Overrides the built-in equals method
    def __eq__(self, other):
        allowable_error = 0.0001
        if isinstance(other, Vector):
            return abs(self.xcoord - other.xcoord) < allowable_error and abs(self.ycoord - other.ycoord) < allowable_error
        return NotImplemented

    # Overrides the built-in not-equals method
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.xcoord + other.xcoord, self.ycoord + other.ycoord)
        else:
            return NotImplemented
        
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.xcoord - other.xcoord, self.ycoord - other.ycoord)
        else:
            return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(self.xcoord*other, self.ycoord*other)
        else:
            return NotImplemented
        
    def __div__(self, other):
        if isinstance(other, Number):
            return Vector(self.xcoord/other, self.ycoord/other)
        else:
            return NotImplemented
        

