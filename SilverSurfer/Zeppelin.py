import threading, Queue, time, ZeppelinControl, Commands, DistanceSensor, GUI

class Zeppelin(threading.Thread):
    
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.command_time = 0
        
        #Make another thread for the Distance Sensor, this eliminates the need to wait for it on height calls
        #TODO: The height has to be logged. It might be a good idea to log it here?
        #Make a distance sensor object here, which inherits from Thread, let it log data continually by making it an infinite loop
        #When zeppelin control needs the data, it can just ask it from the object.
        self.distance_sensor = DistanceSensor.DistanceSensor()
        self.distance_sensor.start() #Start the distance sensor
        
        self.height = 0.0
        
        self.control = ZeppelinControl.ZeppelinControl(self.distance_sensor)
        
    @property
    def height(self):
        return self.distance_sensor.height
         
    def run(self):
        
        while True:
            try:
                command = self.queue.get(False)
                command.execute(self)                
            except Queue.Empty:
                #Do nothing
                pass
            
            #Check if movement needs to be stopped
            if self.command_time - time.time() <= 0:
                self.control.hor_stop()
                
            #self.control.stabilize()
            #Check if the zeppelin is at the right height (+- 10cm)
            error = abs(self.control.current_height-self.control.goal_height) 
            if error <= 10:
                print "At correct height"
                

#Main initialization
command_queue = Queue.Queue()
zeppelin = Zeppelin(queue = command_queue)
gui = GUI.GUI(queue = command_queue, zeppelin = zeppelin)
zeppelin.start()