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
        if(self.zep.navigator.goal_position == 0):
            reply = ('INFO > H:' 
                     + str(height) 
                     +'; GH:' 
                     + str(goal_height) 
                     + '; E:' + str(error) 
                     + '; LM:' + str(left_motor) 
                     + '; RM:' + str(right_motor) 
                     + '; VM:' + str(vert_motor) 
                     +  '; X:' +str(int(self.zep.navigator.position.xcoord))
                     +'; Y:' +str(-1*int(self.zep.navigator.position.ycoord))
                     + '; GX:' + str(int(self.zep.navigator.goal_position))
                     +'; GY:' +str(-1*int(self.zep.navigator.goal_position)))
            
        else:
           reply = ('INFO > H:' 
                     + str(height) 
                     +'; GH:' 
                     + str(goal_height) 
                     + '; E:' + str(error) 
                     + '; LM:' + str(left_motor) 
                     + '; RM:' + str(right_motor) 
                     + '; VM:' + str(vert_motor) 
                     +  '; X:' +str(int(self.zep.navigator.position.xcoord))
                     +'; Y:' +str(-1*int(self.zep.navigator.position.ycoord))
                     + '; GX:' + str(int(self.zep.navigator.goal_position.xcoord))
                     +'; GY:' +str(-1*int(self.zep.navigator.goal_position.ycoord))) 
            
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
    





class PiConn2dot1( threading.Thread, object):
    
    def __init__(self,gate):
        logging.basicConfig()
        threading.Thread.__init__(self)
        self.gate = gate
        adress_server = 'localhost'
        
###########
#Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel(channel_number=1)
        self.channel.exchange_declare(exchange='server', type='topic')

        #Create queues
        info_location = self.channel.queue_declare(queue="info-loc-queue")
        queue_info_location = info_location.method.queue
        
        info_height = self.channel.queue_declare(queue="info-height-queue")
        queue_info_height = info_height.method.queue


        hcommand_move = self.channel.queue_declare(queue="hcommand-move-queue")
        queue_hcommand_move = hcommand_move.method.queue
        
        hcommand_elevate = self.channel.queue_declare(queue="hcommand-elevate-queue")
        queue_hcommand_elevate = hcommand_elevate.method.queue
        
        lcommand_motor1 = self.channel.queue_declare(queue="lcommand-motor1-queue")
        queue_lcommand_motor1 = lcommand_motor1.method.queue
        
        lcommand_motor2 = self.channel.queue_declare(queue="lcommand-motor2-queue")
        queue_lcommand_motor2 = lcommand_motor2.method.queue
        
        lcommand_motor3 = self.channel.queue_declare(queue="lcommand-motor3-queue")
        queue_lcommand_motor3 = lcommand_motor1.method.queue
        
        private =  self.channel.queue_declare(queue="private-queue")
        queue_private = private.method.queue
        
        #bind the queues to keys
        self.channel.queue_bind(exchange='server',queue=queue_info_location,routing_key="*.info.location")
        self.channel.queue_bind(exchange='server',queue=queue_info_height,routing_key="*.info.height")
        self.channel.queue_bind(exchange='server',queue=queue_hcommand_elevate,routing_key="*.hcommand.elevate")
        self.channel.queue_bind(exchange='server',queue=queue_hcommand_move,routing_key="*.hcommand.move")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor1,routing_key="*.lcommand.motor1")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor2,routing_key="*.lcommand.motor2")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor3,routing_key="*.lcommand.motor3")
        self.channel.queue_bind(exchange='server',queue=queue_private,routing_key="*.private.FromPC")
        
        self.channel.basic_consume(self.callback_hcommand_elevate, queue=queue_hcommand_elevate, no_ack=True)
        self.channel.basic_consume(self.callback_hcommand_move, queue=queue_hcommand_move, no_ack=True)
        self.channel.basic_consume(self.callback_private, queue=queue_private, no_ack=True)
###########
        

    def run(self):

            try:
                self.channel.start_consuming()
            except Exception:
                self.connection.close()  

                

    def callback_private(self,ch, method, properties, body):
        reply = self.gate.reply(body)  
        self.send_message_to_gui(reply)  
        
    def callback_hcommand_elevate(self,ch, method, properties, body):
        print "ELEVETATO " + body
        self.gate.elevate(body)   

    def callback_hcommand_move(self,ch, method, properties, body):
        print "GOTO " + body
        self.gate.move_to_horizontal(body)   

    def send_message_to_gui(self,message):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.private.fromPI', body=message)
    
    def send_position_to_server(self,x,y,z):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.info.location', body=str(x)+","+str(y))
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.info.height', body=str(z))
            


            
class Gate2dot1(threading.Thread,object):
    
    def __init__(self, zeppelin):
        threading.Thread.__init__(self)
        self.zep = zeppelin
        self.PIconnection = PiConn2dot1(self)
        self.replies = {'STATUS' : self.status,#Gives the Status of the Pi (Decisions, ...)
                        'INFO' : self.info,  #Gives the Info of the Pi (Height, ...)
                        'SWITCH' : self.switch, #Switches between Auto and Manual mode
                        'SHUTDOWN': self.shutdown, #Shuts the Pi down
                        'CONNECT' : self.connect, #Will tell the PC that the connection is okay
                        'STABILIZE': self.elevate,
 #                       'COMMAND' : self.command,
                        'MOVETO': self.move_to} #Issues commands
      
        
    def open(self):
        #niet meer nodig :)
        #Starts the connection thread
        self.PIconnection.start()
        self.start()
        
    def run(self):
        while(True):
            time.sleep(1.5)
            self.update_server()
    
    def update_server(self):
        self.PIconnection.send_position_to_server(self.zep.navigator.position.xcoord,
                                                   self.zep.navigator.position.ycoord,
                                                    self.zep.navigator.height)
#        self.PIconnection.send_message_to_gui(message)   
    
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
        if(self.zep.navigator.goal_position == 0):
            reply = ('INFO > GH:' 
                     + str(goal_height) 
                     + '; E:' + str(error) 
                     + '; LM:' + str(left_motor) 
                     + '; RM:' + str(right_motor) 
                     + '; VM:' + str(vert_motor) 
                     + '; GX:' + str(int(self.zep.navigator.goal_position))
                     +'; GY:' +str(-1*int(self.zep.navigator.goal_position)))
            
        else:
           reply = ('INFO > GH:' 
                     + str(goal_height) 
                     + '; E:' + str(error) 
                     + '; LM:' + str(left_motor) 
                     + '; RM:' + str(right_motor) 
                     + '; VM:' + str(vert_motor) 
                     + '; GX:' + str(int(self.zep.navigator.goal_position.xcoord))
                     +'; GY:' +str(-1*int(self.zep.navigator.goal_position.ycoord))) 
            
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
    
        
    def move_to(self,request):
       
        com_and_coords = request.split(":")
        coords = com_and_coords[1].split(" ")
        
        self.zep.moveto(int(coords[0]),int(coords[1]),int(coords[2]))
     
        return "moving"
    
    def elevate(self,z):
        if(self.zep.navigator.goal_position == 0):
            self.zep.moveto(self.zep.navigator.position.xcoord,self.zep.navigator.position.ycoord,int(z))
        else:
            self.zep.moveto(self.zep.navigator.goal_position.xcoord,self.zep.navigator.goal_position.ycoord,int(z))
            
    def move_to_horizontal(self,pos):
        coord = pos.split(",")
        self.zep.moveto(int(coord[0]),int(coord[1]),self.zep.navigator.goal_height)
        