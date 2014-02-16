'''
This module contains the class Figure, together with the implementation of colors and strings.

@author     Rob Coekaerts 
@Version    16-2-2014

'''


colors = "blue", "white", "red", "yellow", "black", "green"
shapes = "heart", "oval", "rectangle", "star"
    
'''
checks whether the given color is a valid color.
@return: color in colors
'''
def is_valid_color(color):
    return color in colors

'''
Checks whether the given shape is a valid shape
@return: shape in shapes
'''
def is_valid_shape(shape):
    return shape in shapes



'''
This class represents the figures that are placed at the nodes in a playfield. The objects of this class
are characterised by a shape and a color.

'''
class Figure(object):
    
    '''
    Initialise this figure with a specific shape and color using numbers. 
    @precondition: The given color must be a valid color
                   |is_valid_color(color)
    @precondition: The given shape must be a valid shape
                   |is_valid_shape(shape)
       
    '''
    def __init__(self, color, shape):
        assert is_valid_color(color)
        assert is_valid_shape(shape)
        self.shape = shape
        self.color = color
    

    '''    
    Return a number that identifies the specific figure uniquely.
    '''
    @property
    def figure_id(self):
        decimal = shapes.index(self.shape)
        unit = colors.index(self.color)
        return decimal*10 + unit
    
    
    # Overrides the built-in equals method
    def __eq__(self, other):
        if isinstance(other, Figure):
            return self.figure_id == other.figure_id
        return NotImplemented

    # Overrides the built-in not-equals method
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    