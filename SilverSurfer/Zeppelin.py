import threading, Queue, time

class Zeppelin(threading.Thread):
    
    def __init__(self,queue):
        self.queue = queue
        threading.Thread.__init__(self)
        
    def run(self):
        pass