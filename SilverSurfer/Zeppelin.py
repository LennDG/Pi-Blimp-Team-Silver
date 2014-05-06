import threading
import time
from Vector import Vector
import PiConnection
from Crypto.PublicKey import RSA
     
class Zeppelin(threading.Thread, object):
       
       
    def __init__(self, navigator,name, sim_mode):
        
        threading.Thread.__init__(self)
        
        self.host = '192.168.2.134'
        
        # Assign the navigator object
        self.navigator = navigator
        
        self.sim_mode = sim_mode
        
        # I am going to supply a list of goal positions for now, this is going to change later.
        self.positions = []
#         self.positions.append(Vector(200,-100))
#         self.positions.append(Vector(40,-200))
#         self.positions.append(Vector(200,200))
#         self.positions.append(Vector(40,-200))
        
        self.name = name
        self.gate = PiConnection.Gate2dot1(self)
        self.gate.open()
        
        self.private_key = RSA.generate(1024, e=5)
        self.public_key = self.private_key.publickey().exportKey('PEM')
        
    def moveto(self, x, y, z):
        print "new goal position: " + str(x) + ", " + str(y) + ", " + str(z)
        new_position = Vector(x, y)
        self.navigator.goal_height = z
        self.navigator.goal_position = new_position

             
    def run(self):
        
        
        self.navigator.goal_height = 150
        self.navigator.distance_sensor.height = 150
        
        
        #Start of the zeppelin.
        tablets = {}
        i = 0
        for tablet in self.navigator.field.tablets:
            tablets[i] = (int(tablet.xcoord), int(tablet.ycoord))
            i += 1
            
        while True:

            self.navigator.distance_sensor.calculate_height()
            self.navigator.stabilizer.stabilize()
            
            if self.navigator.goal_height == 0 and self.navigator.height < 20:
                self.navigator.goal_position = 0
            
            if self.navigator.goal_position == 0:
                pass
#                 self.navigator.goal_position = self.positions[i]
#                 i = (i + 1)%4
#                 print "new goal_position: " + str(self.navigator.goal_position.xcoord) + ", "+ str(self.navigator.goal_position.ycoord)
#                 
            
            
            #Logic for QR codes right here
            elif self.navigator.goal_reached:
                print "FIX QR"
                self.navigator.goal_height = 70
                tabletnr = 0
                for i in tablets:
                    print "TABLET I"
                    print tablets[i]
                    print (int(self.navigator.goal_position.xcoord),int(self.navigator.goal_position.ycoord))
                    if tablets[i] == (int(self.navigator.goal_position.xcoord),int(self.navigator.goal_position.ycoord)):
                        tabletnr = i + 1
                
                
                if tabletnr > 0 and tabletnr < 4:
                    print "Send Public Key to tablet"
                    self.gate.PIconnection.send_public_key(self.public_key, tabletnr)
                    if self.sim_mode:

                        text = self.navigator.image_processor.generate_QR_code(self.private_key, filename ='http://'+ self.host+':5000/static/zilver'+str(tabletnr)+'.png') 
                    else:
                        text = self.navigator.image_processor.generate_QR_code(self.private_key)
                    
                    
                    if text == 0:
                        self.navigator.goal_height = 150
                        print "No QR code found"
                    else:
                        text = text.split(':')
                        if text[0] == 'tablet':
                            self.moveto(tablets[int(text[1])-1][0], tablets[int(text[1])-1][1], 150)
                        elif text[0] == 'position':
                            pos = text[1].split(',')
                            self.moveto(pos[0], pos[1], 150)
                elif tabletnr == 0:
                    self.navigator.goal_height = 0
                else:
                    pass
            else:
                pass
