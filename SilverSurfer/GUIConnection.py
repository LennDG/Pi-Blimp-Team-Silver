#File for the GUI connection class, this will be housed on the PC

import socket, threading, Queue

class GUIConn(object):
    
    def __init__(self, input_queue, output_queue):
        
        self.PORT = 8888
        self.PI_IP = "192.168.1.1"
        
        
        try:
            #Creates a socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Socket creating failed, error message:' + str(msg[1])
        
        self.s.connect((self.PI_IP, self.PORT))
        #TODO: Print a socket has been made.
        
        input = Input(input_queue, self.s)
        input.start()
        
        output = Output(output_queue, self.s)
        output.start()
        
    def close(self):
        self.s.close()
        
        
class Input(threading.Thread, object):
    
    def __init__(self, input_queue, socket):
        threading.Thread.__init__(self)
        self.s = socket
        self.queue = input_queue
        
    def run(self):
        while True:
            input = self.s.recv(4096)
            self.queue.put(input)
            
class Output(threading.Thread, object):
    
    def __init__(self, output_queue, socket):
        threading.Thread.__init__(self)
        self.s = socket
        self.queue = output_queue
        
    def run(self):
        while True:
            try:
                output = self.queue.get(False)              
                self.s.sendall(output)
            except Queue.Empty:
                pass
            except socket.error:
                print "Sending failed"
            
            