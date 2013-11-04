import threading, Queue, time, ZeppelinControl, Commands

class Zeppelin(threading.Thread):
    
    def __init__(self,queue):
        self.queue = queue
        self.command_time = 0
        self.control = ZeppelinControl.ZeppelinControl()
        threading.Thread.__init__(self)
        
        
    def run(self):
        
        while True:
            command = self.queue.get()
            if isinstance(command, Commands.TermCommand):
                self.command_time = time.time() + command.calculate_time()
            
            command.execute(self)
            
            if self.command_time - time.time() <= 0:
                self.control.hor_stop()
                
            
                
                
            