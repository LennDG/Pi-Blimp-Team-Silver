import threading
import time
from Vector import Vector
     
class Zeppelin(threading.Thread, object):
       
       
    def __init__(self, navigator,name,sim_mode):
        
        threading.Thread.__init__(self)
        
        # Assign the navigator object
        self.navigator = navigator
        
        # I am going to supply a list of goal positions for now, this is going to change later.
        self.positions = []
        self.positions.append(Vector(200,100))
        self.positions.append(Vector(40,200))
        self.positions.append(Vector(200,200))
        self.positions.append(Vector(40,200))
        
    def moveto(self, x, y, z):
        new_position = Vector(x, y)
        self.navigator.goal_height = z
        self.navigator.goal_position = new_position

             
    def run(self):
        
        self.navigator.goal_height = 150
        self.navigator.distance_sensor.height = 150
        i = 0
        
        while True:
            if self.navigator.goal_height == 0 and self.navigator.height < 20:
                self.navigator.goal_position = 0
            
            if self.navigator.goal_position == 0:
                self.navigator.goal_position = self.positions[i]
                i = (i + 1)%4
                print "new goal_position: " + str(self.navigator.goal_position.xcoord) + ", "+ str(self.navigator.goal_position.ycoord)
                 
                    
            #Logic for QR codes right here
            elif self.navigator.goal_reached :
                #Send Public Key to tablet
                
                #wait half a second
                time.sleep(0.5)
                
                
                text = self.navigator.image_processor.generate_QR_code()
                
                if text == 0: 
                    print "It's not gonna work boys."
                    
                else:
                    print text
                
                #Decrypt text
                
                #Use moveto function to update in navigator
            else:
                time.sleep(1)