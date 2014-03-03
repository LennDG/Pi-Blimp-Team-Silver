'''
Created on 13-feb.-2014

@author: Peter
'''

class Navigator(object):
    '''
    Deze klasse houdt de informatie omtrent de Position van deze Zeppelin bij. Ook de hoek ('Angle') van de zeppelin tov de eenheidsvectoren wordt hier opgeslagen.
    '''


    def __init__(self, distance_sensor, XYCoordInputFiller, angle, Position):
        self.XYCoordInputFiller = "Hier moeten we we nog beslissen of we hier de x- en y- coordinaten gaan berekenen, en wat we hiervoor nodig hebben, of effectief gewoon doorgeven"
        self.distance_sensor = distance_sensor
        self.angle = self.QR.calculate_angle(points, self.QR.QR_images(current_QR)) '''Dit gebeurt later niet meer aan de hand van QR maar adhv de kaart dus moet aangepast worden'''
        self.Position = self.calculate_position(distance_sensor, XYCoordInputFiller)
    
    def calculate_position(self, distance_sensor, XYCoordInputFiller):
        self.position.height = self.distance_sensor.height
        self.position.xcoord = "To be implemented"
        self.position.ycoord = "To be implemented"
        self.position.angle = "To be implemented"
        