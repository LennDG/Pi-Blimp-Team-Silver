#File for the GUI connection class, this will be housed on the PC

import socket

class GUIConn(object):
    
    def __init__(self, GUI):
        
        self.GUI = GUI
        self.PORT = 8888
        self.PI_IP = "192.168.1.1"
        
        try:
            #Creates a socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Socket creating failed, error message:' + str(msg[1])
        
        self.s.connect((self.PI_IP, self.PORT))
        #TODO: Print a socket has been made.
        self.GUI.print_in_textbox("Socket has been made")
        
    def send(self, message):
        #Only takes strings
        try: 
            self.s.sendall(message)
        except socket.error:
            #Something failed
            
        
    def receive(self):
        input = self.s.recv(4096)
        self.GUI.input(input)