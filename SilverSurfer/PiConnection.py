#This is the server file, it is housed on the Pi

import socket, threading, re, Commands,time
import pika, logging

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
            
class PiConn2dot0( threading.Thread, object):
    
    def __init__(self,gate):
        
        threading.Thread.__init__(self)
        self.gate = gate
        adress_server = 'localhost'
        
        #Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
               adress_server))
        self.channel = self.connection.channel()

        #Create Queues
        self.channel.queue_declare(queue='FromGUI')
        self.channel.queue_declare(queue='FromZEP')

        #Callback handles received messages from FromZEP
        self.channel.basic_consume(self.callback,
                      queue='FromGUI',
                      no_ack=True)
        

    def run(self):

            try:
                self.channel.start_consuming()
            except Exception:
                self.connection.close()  

                

    def callback(self,ch, method, properties, body):

        reply = self.gate.reply(body)  
  
        self.send_message_to_gui(reply)    

    def send_message_to_gui(self,message):
        self.channel.basic_publish(exchange='', routing_key='FromZEP', body=message)
            
class Gate(threading.Thread,object):
    
    def __init__(self, zeppelin):
        threading.Thread.__init__(self)
        self.zep = zeppelin
        self.PIconnection = PiConn2dot0(self)
        self.replies = {'STATUS' : self.status,#Gives the Status of the Pi (Decisions, ...)
                        'INFO' : self.info,  #Gives the Info of the Pi (Height, ...)
                        'SWITCH' : self.switch, #Switches between Auto and Manual mode
                        'SHUTDOWN': self.shutdown, #Shuts the Pi down
                        'CONNECT' : self.connect, #Will tell the PC that the connection is okay
                        'STABILIZE': self.stabilize,
                        'COMMAND' : self.command,
                        'MOVETO': self.move_to} #Issues commands
      
        
    def open(self):
        #niet meer nodig :)
        #Starts the connection thread
        self.PIconnection.start()
        self.start()
        
    def run(self):
        while(True):
            time.sleep(1.5)
            self.PIconnection.send_message_to_gui(self.info(" "))
                
    
    def reply(self, request):
        #Looks for the keywords in the request, handles them in the correct way.

        

        if any(word in request for word in self.replies):
            req_word = request.split(":")
            reply= self.replies[req_word[0]](request)
            return reply
        else:
             
            return self.replies['COMMAND'](request)

    def status(self, request):
        reply = 'STATUS > ' + self.zep.STATUS
        return reply
    
    def info(self, request):

        height = int(self.zep.navigator.height)
        goal_height = int(self.zep.navigator.goal_height)
        error = goal_height - height
        
        left_motor = 0 #self.zep.control.motor_control.left_motor.direction
        right_motor = 0 # self.zep.control.motor_control.right_motor.direction
        vert_motor = 0 #self.zep.control.motor_control.vert_motor.level
      
        reply = ('INFO > H:' 
                 + str(height) 
                 +'; GH:' 
                 + str(goal_height) 
                 + '; E:' + str(error) 
                 + '; LM:' + str(left_motor) 
                 + '; RM:' + str(right_motor) 
                 + '; VM:' + str(vert_motor) 
                 + '; X:' +str(int(self.zep.navigator.position.xcoord))
                 +'; Y:' +str(-1*int(self.zep.navigator.position.ycoord)))
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
        commands = {'L' : Commands.ManualTurn(self.zep,1),
                    'R' : Commands.ManualTurn(self.zep,-1),
                    'S' : Commands.VertMove(100),
                    'D' : Commands.VertMove(-100),
                    'V' : Commands.ManualMove(1),
                    'A' : Commands.ManualMove(-1),
                    'STOP':Commands.Stop(self.zep)}
        
        reply = 'Not recognized'
        if any(word in request for word in commands):
            new_command = commands[word]
            new_command.execute()
            reply = 'Executing ' + word
        return reply
        #TODO: find out how to make commands better, because they aren't up to snuff right now! 
        
    def move_to(self,request):
       
        com_and_coords = request.split(":")
        coords = com_and_coords[1].split(" ")
        
        self.zep.moveto(int(coords[0]),int(coords[1]),int(coords[2]))
     
        return "moving"
        