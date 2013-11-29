    

    

import threading, Queue, time, ZeppelinControl, DistanceSensor, sys
     
class Zeppelin(threading.Thread, object):
       
        #TODO: We might have to rewrite A LOT of this code...
       
       
    def __init__(self,queue):
        threading.Thread.__init__(self)
        
        self.STATUS = ''
        
        self.AUTO_MODE = False #This will change some stuff depending on what mode we're in right now.
        
        self.command_queue = queue
        self.command_time = float("inf")
        self.executing_command = None
           
        self.distance_sensor = DistanceSensor.DistanceSensor()
        self.distance_sensor.start() #Start the distance sensor
     
           
        #Hier wordt een zeppelincontrol-object aangemaakt dat we control noemen.
        self.control = ZeppelinControl.ZeppelinControl(self.distance_sensor)
        
           
    def add_command(self, command):
        if command.has_priority():
            while not self.command_queue.empty(): #Clears queue
                try:
                    temp = self.command_queue.get(False)
                except Queue.Empty:
                    pass
            self.command_queue.add(command)
            self.executing_command.is_executed = True
        else:
            self.command_queue.add(command)
           
    @property
    def height(self):
        return self.distance_sensor.height
       
    @height.setter
    def height(self, value):
        self._height = value
             
    def run(self):
           
        while True:
            if  self.command_time < time.time():
                self.executing_command.is_executed = True
                self.command_time = float("inf")
            if self.executing_command.is_executed:
                try:
                    command = self.command_queue.get(False)
                    self.executing_command = command
                    command.execute(self)
                except Queue.Empty:
                    #Do nothing
                    pass
                   
            else:
                pass
                             
            self.control.stabilize()

    def shutdown(self):
        #TODO: This should be a clean shutdown, for now, sys.exit()
        time.sleep(3)
        sys.exit()
                   
     
#Main initialization
command_queue = Queue.Queue()
zeppelin = Zeppelin(queue = command_queue)
zeppelin.start()

