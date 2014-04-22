import threading
import time
from Vector import Vector
import PiConnection
import ImageRecognitionClient as IRC
     
class Zeppelin(threading.Thread, object):
       
       
    def __init__(self, navigator):
        
        threading.Thread.__init__(self)
        
        # Assign the navigator object
        self.navigator = navigator
        
        # I am going to supply a list of goal positions for now, this is going to change later.
        self.positions = []
#         self.positions.append(Vector(200,-100))
#         self.positions.append(Vector(40,-200))
#         self.positions.append(Vector(200,200))
#         self.positions.append(Vector(40,-200))
        

        self.gate = PiConnection.Gate2dot1(self)
        self.gate.open()
        self.IRC = IRC()
        
    def moveto(self, x, y, z):
        new_position = Vector(x, y)
        self.navigator.goal_height = z
        self.navigator.goal_position = new_position

             
    def run(self):
        
        self.navigator.goal_height = 150
        self.navigator.distance_sensor.height = 150
        
        while True:
            if self.navigator.goal_height == 0 and self.navigator.height < 20:
                self.navigator.goal_position = 0
            
            if self.navigator.goal_position == 0:
                pass
#                 self.navigator.goal_position = self.positions[i]
#                 i = (i + 1)%4
#                 print "new goal_position: " + str(self.navigator.goal_position.xcoord) + ", "+ str(self.navigator.goal_position.ycoord)
#                 
                    
            #Logic for QR codes right here
            elif self.navigator.goal_reached :
                #Send Public Key to tablet
                
                #wait half a second
                time.sleep(0.5)
                
                #Start a timer
                tic = time.time()
                
                #Take picture
                self.IRC.take_picture("/run/shm/QR.jpg")
                
                #Read text
                text = self.decode_qrcode("/run/shm/QR.jpg")
                
                #Keep trying to take picture for 5 seconds if it is not found
                while text is None:
                    self.take_picture("/run/shm/QR.jpg")
                    text = self.decode_qrcode("/run/shm/QR.jpg")
                    if time.time() - tic > 5:
                        #Can't read QR code, stop trying
                        break
                
                #Decrypt text
                
                #Use moveto function to update in navigator
            else:
                time.sleep(1)