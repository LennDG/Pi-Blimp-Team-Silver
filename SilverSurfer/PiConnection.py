#This is the server file, it is housed on the Pi

import socket, threading, time

class PiConn(threading.Thread, object):
    
    def __init__(self, gate):
        threading.Thread.__init__(self)
        
        HOST = ''
        PORT = 8888
        
        self.gate = gate
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

    def run(self):
        self.s.listen(1)
        conn, addr = self.s.accept() #BLOCKING CALL
        print 'Connected by', addr
        try:
            while True:
                request = conn.recv(1024) #BLOCKING CALL
                if not request: break
                reply = self.gate.reply(request)
                conn.sendall(reply)
            conn.close()
        except Exception:
            conn.close()
            
class Gate(object):
    global KEYWORDS
    KEYWORDS = ['STATUS', 'INFO', 'SWITCH', 'SHUTDOWN']
    
    
    def __init__(self, zeppelin):
        self.zep = zeppelin
        connection = PiConn(self)
        connection.start()
    
    def reply(self, request):
        request_type = self.keyword_check(request)
        
        replies = {'STATUS' : self.status,#Gives the Status of the Pi (Decisions, ...)
                   'INFO' : self.info,  #Gives the Info of the Pi (Height, ...)
                   'SWITCH' : self.switch, #Switches between Auto and Manual mode
                   'SHUTDOWN': self.shutdown, #Shuts the Pi down
                   'COMMAND' : self.command} #Issues commands
        
        return replies[request_type](request)
        
    
    def keyword_check(self, request):
        #Checks if one of the keywords is in the request, if so, returns the word. Else returns the string 'COMMAND'
        if any(word in request for word in KEYWORDS):
            return word
        else:
            return 'COMMAND'
            
    def status(self, request):
        reply = 'STATUS > ' + self.zep.STATUS
        return reply
    
    def info(self, request):
        height = self.zep.height
        goal_height = self.zep.goal_height
        error = goal_height - height
        
        left_motor = self.zep.control.motor_control.left_motor.direction
        right_motor = self.zep.control.motor_control.right_motor.direction
        vert_motor = self.zep.control.motor_control.vert_motor.level
        
        reply = 'INFO > H:' + height +' G:' + goal_height + ' E:' + error + ' LM:' + left_motor + ' RM:' + right_motor + ' VM:' + vert_motor
        return reply
    
    def switch(self, request):
        if self.zep.AUTO_MODE:
            self.zep.AUTO_MODE = False
            reply = 'SWITCH > MANUAL MODE' #If wanted, this reply can change
            return reply
        else:
            self.zep.AUTO_MODE = True
            reply = 'SWITCH > AUTOMATIC MODE'
            return reply
        
    def shutdown(self, request):
        reply = 'SHUTDOWN > SHUTTING DOWN IN 3 SECONDS'
        return reply
        self.zep.shutdown() #This method waits 3 seconds
    
    def command(self, request):
        reply = request + ' > Processing commands and executing them !!!!!!!!!NOT YET IMPLEMENTEDs!!!!!!!!!!!'
        return reply
        #TODO: find out how to make commands better, because they aren't up to snuff right now!
        pass 