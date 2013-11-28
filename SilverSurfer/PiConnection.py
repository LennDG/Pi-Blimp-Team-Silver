#This is the server file, it is housed on the Pi

import socket, threading

class Server(threading.Thread, object):
    
    def __init__(self, inqueue, outqueue):
        threading.Thread.__init__(self)
        
        HOST = ''
        PORT = 8888
        
        self.inqueue = inqueue
        self.outqueue = outqueue
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

    def run(self):
        self.s.listen(1)
        conn, addr = self.s.accept() #BLOCKING CALL
        print 'Connected by', addr
        try:
            while True:
                data = conn.recv(1024) #BLOCKING CALL
                if not data: break
                self.inqueue.put(data)
                reply = self.outqueue.get(True) #BLOCKING CALL
                conn.sendall(reply)
            conn.close()
        except Exception:
            conn.close()
            
