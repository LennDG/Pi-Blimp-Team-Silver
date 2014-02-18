from math import sqrt, acos

class Vector(object):
    
    
    def __init__(self, xcoord, ycoord):
        self.xcoord = xcoord
        self.ycoord = ycoord
    
    #hoek van 0..2*Pi
    @property    
    def angle(self):
        x_vector = Vector(1,0)
        return acos(self.inner_product(x_vector)/self.norm())
        
    @property    
    def norm(self):
        return sqrt(self.xcoord**2 + self.ycoord**2)
    
    def inner_product(self, other):
        X = self.xcoord*other.xcoord
        Y = self.ycoord*other.ycoord
        return X + Y
    
    
