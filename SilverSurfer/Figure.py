'''
This class represents the figures that are placed at the nodes in a playfield. The objects of this class
are characterised by a shape and a color.

@author     Rob Coekaerts 
@Version    16-2-2014

'''
class Figure(object):
    
    '''
    Initialise this figure with a specific shape and color using numbers. 
    Colors are represented in the following way: 
       blue = 1, white = 2, red = 3, yellow = 4, black = 5, green = 6.
    Shapes are represented in the following way:
       heart = 1, oval = 2, rectangle = 3, star = 4.
       
    '''
    def __init__(self, shape, color):
        self._shape = shape
        self._color = color
    
    '''
    Return the shape of this object using a number.
      1 = heart, 2 = oval, 3 = rectangle, 4 = star 
    '''  
    @property    
    def shape(self):
        return self._shape
    
    '''
    Return the color of this object using a number.
      1 = blue, 2 = white, 3 = red, 4 = yellow, 5 = black, 6 = green. 
    '''  
    @property
    def color(self):
        return self._color
    
    '''
    Return a number that identifies the specific figure uniquely.
    @return: self.shape*10 + self.color
    '''
    def identity(self):
        return self.shape*10 + self.color
    