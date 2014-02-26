from math import sqrt, asin, acos, pi, copysign

class Vector(object):
    
    
    def __init__(self, xcoord, ycoord):
        self.xcoord = xcoord
        self.ycoord = ycoord
    
    #hoek van -pi...pi
    @property    
    def angle(self):
        angle = asin(self.ycoord/self.norm)
        if self.xcoord >= 0:
            pass
        elif self.ycoord >= 0:
            angle = pi - angle 
        else:
            angle = -pi - angle
        return angle
             
        
    @property
    #Retrieves the length of the vector    
    def norm(self):
        return sqrt(self.xcoord**2 + self.ycoord**2)
    
    def inner_product(self, other):
        X = self.xcoord*other.xcoord
        Y = self.ycoord*other.ycoord
        return X + Y
