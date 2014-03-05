import threading, time, Navigator, DistanceSensor, CSV_parser, Field
     
class Zeppelin(threading.Thread, object):
       
       
    def __init__(self, field):
        row_0 = "XX,XX,RH,GC,WC,RH,XX\n"
        row_1 = "XX,BH,RH,WS,WR,YS,XX\n"
        row_2 = "XX,BR,YH,RH,GS,GC,YH\n"
        row_3 = "BS,RS,GC,BS,BH,BC,GS\n"
        row_4 = "XX,RR,YR,GH,WC,BH,WR\n"
        row_5 = "XX,WR,YS,BC,WS,GR,XX\n"
        
        row_6 = "XX,XX,GH,RS,BC,GR,XX\n"
        
        field = row_0 + row_1 + row_2 + row_3 + row_4 + row_5 + row_6
        threading.Thread.__init__(self)
        
        parser = CSV_parser.CSV_parser()
        field = parser.parse(field)
        self.field = Field.Field(field)
        
        self.distance_sensor = 0
        # self.distance_sensor = DistanceSensor.DistanceSensor()
        # self.distance_sensor.start() #Start the distance sensor
        
        #Hier wordt een navigator-object aangemaakt
        self.navigator = Navigator.Navigator(self.distance_sensor, field.top_left_node)
        
        # Voorlopig maken we hier een doelpositie aan omdat we nog geen connectie hebben.     
             
    def run(self):
        
        while True:
            
            
            if self.navigator.goal_position == 0:
                pass # Do nothing
            # Hier gaat nog iets komen van langs de receiving kant van de server
            
            else:
                if self.navigator.goal_position == self.navigator.position:
                    self.navigator.land()
                else:
                    # take picture
                    
                    # decode picture
                    # will result in figure_images, other data and a timestamp
                    figure_images = 0
                    other_data = 0
                    time = 0
                    
                    # Extract the triangle of figures out of the data provided
                    figures = Field.extract_triangle(figure_images)
                    
                    # match triangle in field
                    nodes = self.field.find_triangle(figures)
                    
                    # update state
                    self.navigator.update(nodes[0], other_data[0], nodes[1], other_data[1], nodes[2], other_data[2], time)
                    
                    # update motorcontrol
                    self.navigator.update_motors()
                    
                    pass
            
                    
                                    
            

