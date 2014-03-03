'''
Created on 13-feb.-2014

@author: Peter
'''

class Position(object):
    ''' Klasse die de positie bijhoudt van de zeppelin in X, Y en Z-coordinaten (X = links/rechts, Y= vooruit/achteruit, Z=hoogte),
    de klasse berekent of meet zelf  niets'''

    

    def __init__(self, xcoord, ycoord, height):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.height = height
        
    @property
    def xcoord(self):
        return self._xcoord
    @property
    def ycoord(self):
        return self._ycoord
    @property
    def height(self):
        return self._height