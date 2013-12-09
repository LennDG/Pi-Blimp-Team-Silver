#This is the server file, it is housed on the Pi

import socket, threading, re, Commands

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
    
    def __init__(self, zeppelin):
        self.zep = zeppelin
        self.connection = PiConn(self)
        
        self.replies = {'STATUS' : self.status,#Gives the Status of the Pi (Decisions, ...)
                        'INFO' : self.info,  #Gives the Info of the Pi (Height, ...)
                        'SWITCH' : self.switch, #Switches between Auto and Manual mode
                        'SHUTDOWN': self.shutdown, #Shuts the Pi down
                        'CONNECT' : self.connect, #Will tell the PC that the connection is okay
                        'STABILIZE': self.stabilize,
                        'COMMAND' : self.command} #Issues commands
        
    def open(self):
        #Starts the connection thread
        self.connection.start()
    
    def reply(self, request):
        #Looks for the keywords in the request, handles them in the correct way.
        if any(word in request for word in self.replies):
            return self.replies[word](request)
        else:
            
            return self.replies['COMMAND'](request)

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
        
        reply = 'INFO > H:' + height +'; GH:' + goal_height + '; E:' + error + '; LM:' + left_motor + '; RM:' + right_motor + '; VM:' + vert_motor
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
        
    def connect(self, request):
        reply = 'CONNECT > CONNECTION ESTABLISHED'
        return reply
    
    def stabilize(self, request):
        height = re.search('(\d+)', request)
        self.zep.goal_height = height.group(1)
        if height.group(1) <= 0:
            self.zep.stabilize(False)
            reply = 'STABILIZE > STOPPING STABILIZE'
        else:
            self.zep.stabilize(True)
            reply = 'STABILIZE > STABILIZING ON: ' + str(height.group(1))
        return reply
    
    def command(self, request):
        commands = {'L' : Commands.ManualTurn(1),
                    'R' : Commands.ManualTurn(-1),
                    'S' : Commands.VertMove(100),
                    'D' : Commands.VertMove(-100),
                    'V' : Commands.ManualMove(1),
                    'A' : Commands.ManualMove(-1)}
        
        if any(word in request for word in commands):
            new_command = commands[word]
            new_command.execute()
        reply = request + ' > Processing commands and executing them !!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!'
        return reply
        #TODO: find out how to make commands better, because they aren't up to snuff right now! 