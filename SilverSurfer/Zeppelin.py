
import threading, time, ZeppelinControl, DistanceSensor, sys, PiConnection, QR, re, Compiler, Commands
     
class Zeppelin(threading.Thread, object):
       
        #TODO: We might have to rewrite A LOT of this code...
       
       
    def __init__(self,queue):
        threading.Thread.__init__(self)
        
        self.STATUS = ''
        
        self.AUTO_MODE = False #This will change some stuff depending on what mode we're in right now.
        
        self.compiler = Compiler.Commandfactory(self)
        self.command_time = float("inf")
        self.executing_command = None
           
        self.distance_sensor = DistanceSensor.DistanceSensor()
        self.distance_sensor.start() #Start the distance sensor
        
        self._goal_height = 1.0
        self.goal_angle = 0.0 #This is the nominal angle, in degrees
        self.goal_distance = 0.0 #5.9*2*distance + offset is the time needed.
     
           
        #Hier wordt een zeppelincontrol-object aangemaakt dat we control noemen.
        self.control = ZeppelinControl.ZeppelinControl(self.distance_sensor)
        self.QR = QR.QR(self)
        self.QR.start()
        
        gate = PiConnection.Gate(self)
        gate.open() #Starts looking for the first signs of connection.
        
    @property
    def height(self):
        return self.distance_sensor.height 
    
    @property
    def goal_height(self):
        return self._goal_height
    
    @goal_height.setter
    def goal_height(self, value):
        self._goal_height = value
        self.control.goal_height = value
           
    def stabilize(self, on):
        if on is True:
            self.control.stabilize()
        else:
            self.control.end_stabilize()       
             
    def run(self): 
        QR_executed = {}#Dictionary of QR numbers and whether they are executed already
        current_QR = 1 #The QR that is currently being executed, starts at 1
        command_list = []
        
        while True:                
            if not self.AUTO_MODE:
                #Manual stuff
                pass
            else:
                #Auto stuff
                if max(self.QR.QR_codes) > current_QR: #New QR code found
                    #TODO: STOP CURRENT COMMANDS HERE
                    current_QR = max(self.QR.QR_codes)
                    #get the points 
                    while self.QR.QR_points[current_QR] is None:
                        time.sleep(0.2)
                    points = self.QR.QR_points[current_QR]
                    #get the angle
                    angle = self.QR.calculate_angle(points, self.QR.QR_images(current_QR))
                    #Calculate difference with goal angle
                    angle_error = self.goal_angle - angle
                    #Parse the commands
                    command_list = self.compiler.create_commands(self.QR_codes[current_QR])
                    #Make extra command for turning and put on top of list
                    #TODO: make turn command
                    turn_command = Commands.Turn(False, angle_error, self)
                    command_list.insert(0, turn_command)
                    #Get new goal angle
                    L_angle = re.search('L:(\d+)', self.QR.QR_codes(current_QR)).group(1)
                    R_angle = re.search('R:(\d+)', self.QR.QR_codes(current_QR)).group(1)
                    if L_angle is not None:
                        self.goal_angle += int(L_angle)
                    if R_angle is not None:
                        self.goal_angle -= int(R_angle)
                        
            #Execute commands, either the new ones, or the ones executing
            #Executes commands in sequence by using i as an index
            i = 0
            self.STATUS = 'Executing QR ' + current_QR
            while i < len(command_list) and not self.QR.new_QR_scanned:
                self.executing_command = command_list[i]#New command
                if self.executing_command is not self.executing_command.is_executed: #check if the command is already executed
                    if not self.executing_command.is_alive(): #If it is not, start it.
                        self.executing_command.start()
                else:
                    i = i + 1


    def shutdown(self):
        #TODO: This should be a clean shutdown, for now, sys.exit()
        time.sleep(3)
        sys.exit()


