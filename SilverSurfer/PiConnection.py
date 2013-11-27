#File for the Pi connection class, this will be housed on the Pi

import socket, threading, Queue

class PiConn(object):
    
    def __init__(self, input_queue, output_queue):
        self.HOST = ''
        self.PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error, msg:
            print "Binding socket failed, error message: " + msg[1]
            
        
        
        inbox = Input(input_queue, self.s)
        inbox.start()
    
    def start(self):
        self.s.listen(1)
        
    def stop(self):
        self.s.close()
    
class Input(threading.Thread, object):
    
    def __init__(self, input_queue, socket):
            threading.Thread.__init__(self)
            self.queue = input_queue
            self.s = socket
            

    def run(self):
        while True:
            conn = self.s.accept()
            data = conn.recv(1024)
            self.queue.put(data)
        
class Output(threading.Thread, object):
        
        def __init__(self, output_queue, socket):
            threading.Thread.__init__(self)
            self.queue = output_queue
            self.s = socket
            
        def run(self):
            while True:
                try:
                    output = self.queue.get(False)              
                    self.s.sendall(output)
                except Queue.Empty:
                    pass
                except socket.error:
                    print "Sending failed"
            