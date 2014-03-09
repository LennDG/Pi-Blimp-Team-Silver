import threading
import time
from Vector import Vector
     
class Zeppelin(threading.Thread, object):
       
       
    def __init__(self, navigator):
        
        threading.Thread.__init__(self)
        
        # Assign the navigator object
        self.navigator = navigator
        
        # I am going to supply a list of goal positions for now, this is going to change later.
        self.positions = []
        self.positions.append(Vector(2,-1))
        self.positions.append(Vector(0.4,-2))
        self.positions.append(Vector(2,2))
        self.positions.append(Vector(0.4,-2))
             
    def run(self):
        
        i = 0
        self.navigator.goal_height = 150
        self.navigator.distance_sensor.height = 150
        
        while True:
            
            if self.navigator.goal_position == 0:
                self.navigator.goal_position = self.positions[i]
                i = (i + 1)%4
                print "new goal_position: " + str(self.navigator.goal_position.xcoord) + ", "+ str(self.navigator.goal_position.ycoord)
                
            elif self.navigator.goal_reached == True:
                self.navigator.goal_position = self.positions[i]
                i = (i + 1)%4
                print "new goal_position: " + str(self.navigator.goal_position.xcoord) + ", "+ str(self.navigator.goal_position.ycoord)
                
            else:
                time.sleep(1)