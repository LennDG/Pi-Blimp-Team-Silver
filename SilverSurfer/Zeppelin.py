
import threading, time, ZeppelinControl, DistanceSensor, sys, PiConnection, QR, re, Compiler, Commands
     
class Zeppelin(threading.Thread, object):
       
        #TODO: We might have to rewrite A LOT of this code...
       
       
    def __init__(self):
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
        if on:
            self.control.stabilize()
        else:
            self.control.end_stabilize()       
             
    def run(self): 
        current_QR = 0 #The QR that is currently being executed, starts at 1
        command_list = []
        index = 0
        self.stabilize(True)
        self.STATUS = 'Waiting for first QR'
        while True:
            if current_QR < max(self.QR.QR_codes):
                current_QR = max(self.QR.QR_codes)
                command_list = self.compiler.create_commands(self.QR.QR_codes[current_QR])
                self.STATUS = 'Executing QR number ' + str(current_QR) + ': ' + self.QR.QR_codes[current_QR] + '\n Executing command 1'
                command_list[index].start()
            if current_QR is 0: 
                continue                          
            if command_list[index].is_executed and index + 1 < len(command_list):
                index += 1
                self.STATUS = 'Executing command: ' + str(index)
                command_list[index].start()               
            else:
                time.sleep(0.3)
                            
            


    def shutdown(self):
        #TODO: This should be a clean shutdown, for now, sys.exit()
        time.sleep(3)
        sys.exit()


