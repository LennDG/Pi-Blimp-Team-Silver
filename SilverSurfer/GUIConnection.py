#This is the client conneciton side, housed on PC

import socket, threading

class GUIConn(threading.Thread, object):
    
    def __init__(self, inqueue, outqueue):
        threading.Thread.__init__(self)
        
        HOST = '192.168.1.1'
        PORT = 8888
        
        self.inqueue= inqueue
        self.outqueue = outqueue
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        
    def run(self):
        while True:
            try:
                data = self.outqueue.get(True) #BLOCKING CALL
                self.s.sendall(data)
                reply = self.s.recv(1024) #BLOCKING CALL
                self.inqueue.put(reply)
            except Exception:
                self.s.close()
                