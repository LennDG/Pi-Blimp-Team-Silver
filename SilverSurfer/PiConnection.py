#This is the server file, it is housed on the Pi

import socket, threading, re, Commands,time
import pika, logging,random

class PiConn2dot1( threading.Thread, object):
    
    def __init__(self,gate):
        logging.basicConfig()
        threading.Thread.__init__(self)
        self.gate = gate
        
        
        credentials = pika.PlainCredentials('zilver', 'zilver')
        self.parameters = pika.ConnectionParameters(host = 'localhost', port = 5673, credentials= credentials)
#        self.parameters = 'localhost'
        
        not_established = True
        while(not_established):
             try:
                 self.initialization_sender()
                 self.initialization_receiver()

                 not_established = False
             except Exception:
                 not_established = True
        

###########
        

    def run(self):
        thrown = False
        
        while True:
            try:
                if thrown == False:
                    print "pre testing reinitialization consumer"
                    thrown = True
                    raise Exception
                self.channel_consumer.start_consuming()
            except Exception:
                print "PI consumer reinitializated"
                self.initialization_receiver() 
                
    def initialization_sender(self):
        self.connection_sender = pika.BlockingConnection(self.parameters)
        self.channel_sender = self.connection_sender.channel(channel_number=2)
        self.channel_sender.exchange_declare(exchange='server', type='topic')

    def initialization_receiver(self):
        

        
###########
#Make channel_consumer
        self.connection_consumer = pika.BlockingConnection( self.parameters)
        self.channel_consumer = self.connection_consumer.channel(channel_number=1)
        self.channel_consumer.exchange_declare(exchange='server', type='topic')


        hcommand_move = self.channel_consumer.queue_declare(queue="hcommand-move-silver")
        self.queue_hcommand_move = hcommand_move.method.queue
        
        hcommand_elevate = self.channel_consumer.queue_declare(queue="hcommand-elevate-silver")
        self.queue_hcommand_elevate = hcommand_elevate.method.queue
        
        lcommand_motor1 = self.channel_consumer.queue_declare(queue="lcommand-motor1-silver")
        self.queue_lcommand_motor1 = lcommand_motor1.method.queue
        
        lcommand_motor2 = self.channel_consumer.queue_declare(queue="lcommand-motor2-silver")
        self.queue_lcommand_motor2 = lcommand_motor2.method.queue
        
        lcommand_motor3 = self.channel_consumer.queue_declare(queue="lcommand-motor3-silver")
        self.queue_lcommand_motor3 = lcommand_motor1.method.queue
         
        private_setpid =  self.channel_consumer.queue_declare(queue="private-setpid-silver")
        self.queue_private_setpid = private_setpid.method.queue
                #bind the queues to keys
#         self.channel_consumer.queue_bind(exchange='server',queue=queue_info_location,routing_key="*.info.location")
#         self.channel_consumer.queue_bind(exchange='server',queue=queue_info_height,routing_key="*.info.height")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_hcommand_elevate,routing_key="silversurfer.hcommand.elevate")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_hcommand_move,routing_key="silversurfer.hcommand.move")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_lcommand_motor1,routing_key="silversurfer.lcommand.motor1")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_lcommand_motor2,routing_key="silversurfer.lcommand.motor2")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_lcommand_motor3,routing_key="silversurfer.lcommand.motor3")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_setpid,routing_key="silversurfer.private.pid.setpid")
        
        self.channel_consumer.basic_consume(self.callback_hcommand_elevate, queue=self.queue_hcommand_elevate, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_hcommand_move, queue=self.queue_hcommand_move, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_setpid, queue=self.queue_private_setpid, no_ack=True)   
        self.channel_consumer.basic_consume(self.callback_set_motor1, queue=self.queue_lcommand_motor1, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_set_motor2, queue=self.queue_lcommand_motor2, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_set_motor3, queue=self.queue_lcommand_motor3, no_ack=True)        

    def callback_private_setpid(self,ch, method, properties, body):
        params = body.split(" ")
        for param in params:
            p = param.split("=")
            self.gate.set_PID_parameter(p[0],p[1])
            
    def send_PID_param(self):

        message = ("Ci="+str(self.gate.zep.navigator.stabilizer.Ci)
                   +" Cd=" +str(self.gate.zep.navigator.stabilizer.Cd)
                   +" Kp=" +str(self.gate.zep.navigator.stabilizer.Kp)
                   +" Kd=" +str(self.gate.zep.navigator.stabilizer.Kd)
                   +" Ki=" +str(self.gate.zep.navigator.stabilizer.Ki)
                   +" BIAS="+str(self.gate.zep.navigator.stabilizer.BIAS)
                   +"MAX_PID_OUTPUT="+str(self.gate.zep.navigator.stabilizer.MAX_PID_OUTPUT)
                   +"MAX_Ci="+str(self.gate.zep.navigator.stabilizer.MAX_Ci))
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.pid.infofromzep', body=message)
            
        
    def callback_set_motor1(self,ch, method, properties, body):
        self.gate.set_motor1(body)
        
    def callback_set_motor2(self,ch, method, properties, body):
        self.gate.set_motor2(body)
        
    def callback_set_motor3(self,ch, method, properties, body):
        self.gate.set_motor3(body)
        
    def callback_hcommand_elevate(self,ch, method, properties, body):
        print "ELEVETATO " + body
        self.gate.elevate(body)   

    def callback_hcommand_move(self,ch, method, properties, body):
        print "GOTO " + body
        self.gate.move_to_horizontal(body)   

    def send_message_to_gui(self,message):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.fromPI', body=message)
    
    def send_position_to_server(self,x,y,z):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.info.location', body=str(x)+","+str(y))
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.info.height', body=str(z))
            
    def send_status(self,status):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.status', body=status)
        
    def send_goal_coordinates(self,x,y,z):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.goalcoords', body=str(x)+","+str(y)+","+str(z))
        
    def send_coords_figures(self,string):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.recognized', body=string)
        
    def send_info_motors(self,string):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.private.motors', body=string)
        
    def send_public_key_to(self,tabletnb,key):
        self.channel_sender.basic_publish(exchange='server', routing_key='silversurfer.tablets.tablet'+str(tabletnb), body=key)

            
class Gate2dot1(threading.Thread,object):
    
    def __init__(self, zeppelin):
        print "initiate gate"
        threading.Thread.__init__(self)
        self.zep = zeppelin
        self.PIconnection = PiConn2dot1(self)
        self.PID_dict = {"Kp":self.set_Kp,
                         "Kd":self.set_Kd,
                         "Ki":self.set_Ki,
                         "Ci":self.set_Ci,
                         "Cd":self.set_Cd,
                         "BIAS": self.set_BIAS,
                         "MAX_PID_OUTPUT":self.set_MAX_PID_OUTPUT,
                         "MAX_Ci":self.set_MAX_Ci}
        
        #coords for testing purposes
        self.coords = ["10,10","30,30;60,60;60,70","30,30;100,100","100,100;30,30;200,200;10,10;40,40"]
        
    def set_PID_parameter(self,param,val):
        try:
            self.PID_dict[param](float(val))
        except Exception:
            pass

      
        
    def open(self):
        print "Open connection Pi-side"
        self.PIconnection.start()
        self.start()
    
    #TODO: HIER LOOPT HET SOMS FOUT
    def run(self):
        thrown = False
        while True:
            try:
                if thrown == False:
                    print "pre testing reinitialization sender"
                    thrown = True
                    raise Exception
                time.sleep(1.5)
                self.update_server()
            except Exception:
                print "PI sender reinitializated"
                self.PIconnection.initialization_sender() 
    
    def update_server(self):
        self.PIconnection.send_position_to_server(self.zep.navigator.position.xcoord,
                                                   self.zep.navigator.position.ycoord,
                                                    self.zep.navigator.height)
        if self.zep.navigator.goal_position != 0:
            self.PIconnection.send_goal_coordinates(self.zep.navigator.goal_position.xcoord, self.zep.navigator.goal_position.ycoord, self.zep.navigator.goal_height)
    
        rand = int(random.uniform(0,len(self.coords)))
        self.PIconnection.send_coords_figures(self.coords[rand])
        m1 = self.zep.navigator.motor_control.left_motor.level
        m2 = self.zep.navigator.motor_control.right_motor.level
        m3 = self.zep.navigator.motor_control.vert_motor.level
        self.PIconnection.send_info_motors(str(m1)+" "+str(m2)+" "+str(m3))
        self.PIconnection.send_PID_param()
        
        

    
        
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
        
    def set_motor1(self,string):
        a = (int(float(string)))
        if(a >= -100 and a <= 100):
            self.zep.navigator.motor_control.left_motor.level=a
        
    def set_motor2(self,string):
        lvl= (int(float(string)))
        if(lvl >= -100 and lvl <= 100):
            self.zep.navigator.motor_control.right_motor.level=lvl
        
    def set_motor3(self,string):
        lvl= (int(float(string)))
        if(lvl >= -100 and lvl <= 100):
            self.zep.navigator.motor_control.vert_motor.level=lvl

    def set_Kp(self,kp):
        self.zep.navigator.stabilizer.Kp=kp
    def set_Kd(self,kd):
        self.zep.navigator.stabilizer.Kd=kd
    def set_Ki(self,ki):
        self.zep.navigator.stabilizer.Ki=ki
    def set_Ci(self,ci):
        self.zep.navigator.stabilizer.Ci=ci
    def set_Cd(self,cd):
        self.zep.navigator.stabilizer.Cd=cd
    def set_BIAS(self,bias):
        self.zep.navigator.stabilizer.BIAS=bias
    def set_MAX_PID_OUTPUT(self,max_pid):
        self.zep.navigator.stabilizer.MAX_PID_OUTPUT=kp
    def set_MAX_Ci(self,max_ci):
        self.zep.navigator.stabilizer.MAX_Ci = max_ci
    
# class PiConn(threading.Thread, object):
#     
#     def __init__(self, gate):
#         threading.Thread.__init__(self)
#         
#         HOST = ''
#         PORT = 8888
#         
#         self.gate = gate
#         
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.s.bind((HOST, PORT))
# 
#     def run(self):
#         self.s.listen(1)
#         conn, addr = self.s.accept() #BLOCKING CALL
#         print 'Connected by', addr
#         try:
#             while True:
#                 request = conn.recv(1024) #BLOCKING CALL
#                 if not request: break
#                 reply = self.gate.reply(request)
#                 conn.sendall(reply)
#             conn.close()
#         except Exception:
#             conn.close()
#             
# class PiConn2dot0( threading.Thread, object):
#     
#     def __init__(self,gate):
#         
#         threading.Thread.__init__(self)
#         self.gate = gate
#         adress_server = 'localhost'
#         
#         #Make channel_consumer
#         self.connection_consumer = pika.BlockingConnection(pika.ConnectionParameters(
#                adress_server))
#         self.channel_consumer = self.connection_consumer.channel_consumer()
# 
#         #Create Queues
#         self.channel_consumer.queue_declare(queue='FromGUI')
#         self.channel_consumer.queue_declare(queue='FromZEP')
# 
#         #Callback handles received messages from FromZEP
#         self.channel_consumer.basic_consume(self.callback,
#                       queue='FromGUI',
#                       no_ack=True)
#         
# 
#     def run(self):
# 
#             try:
#                 self.channel_consumer.start_consuming()
#             except Exception:
#                 self.connection_consumer.close()  
# 
#                 
# 
#     def callback(self,ch, method, properties, body):
# 
#         reply = self.gate.reply(body)  
#   
#         self.send_message_to_gui(reply)    
# 
#     def send_message_to_gui(self,message):
#         self.channel_consumer.basic_publish(exchange='', routing_key='FromZEP', body=message)
#             
# class Gate(threading.Thread,object):
#     
#     def __init__(self, zeppelin):
#         threading.Thread.__init__(self)
#         self.zep = zeppelin
#         self.PIconnection = PiConn2dot0(self)
#         self.replies = {'STATUS' : self.status,#Gives the Status of the Pi (Decisions, ...)
#                         'INFO' : self.info,  #Gives the Info of the Pi (Height, ...)
#                         'SWITCH' : self.switch, #Switches between Auto and Manual mode
#                         'SHUTDOWN': self.shutdown, #Shuts the Pi down
#                         'CONNECT' : self.connect, #Will tell the PC that the connection_consumer is okay
#                         'STABILIZE': self.stabilize,
#                         'COMMAND' : self.command,
#                         'MOVETO': self.move_to} #Issues commands
#       
#         
#     def open(self):
#         #niet meer nodig :)
#         #Starts the connection_consumer thread
#         self.PIconnection.start()
#         self.start()
#         
#     def run(self):
#         while(True):
#             time.sleep(1.5)
#             self.PIconnection.send_message_to_gui(self.info(" "))
#                 
#     
#     def reply(self, request):
#         #Looks for the keywords in the request, handles them in the correct way.
# 
#         
# 
#         if any(word in request for word in self.replies):
#             req_word = request.split(":")
#             reply= self.replies[req_word[0]](request)
#             return reply
#         else:
#              
#             return self.replies['COMMAND'](request)
# 
#     def status(self, request):
#         reply = 'STATUS > ' + self.zep.STATUS
#         return reply
#     
#     def info(self, request):
# 
#         height = int(self.zep.navigator.height)
#         goal_height = int(self.zep.navigator.goal_height)
#         error = goal_height - height
#         
#         left_motor = 0 #self.zep.control.motor_control.left_motor.direction
#         right_motor = 0 # self.zep.control.motor_control.right_motor.direction
#         vert_motor = 0 #self.zep.control.motor_control.vert_motor.level
#         if(self.zep.navigator.goal_position == 0):
#             reply = ('INFO > H:' 
#                      + str(height) 
#                      +'; GH:' 
#                      + str(goal_height) 
#                      + '; E:' + str(error) 
#                      + '; LM:' + str(left_motor) 
#                      + '; RM:' + str(right_motor) 
#                      + '; VM:' + str(vert_motor) 
#                      +  '; X:' +str(int(self.zep.navigator.position.xcoord))
#                      +'; Y:' +str(-1*int(self.zep.navigator.position.ycoord))
#                      + '; GX:' + str(int(self.zep.navigator.goal_position))
#                      +'; GY:' +str(-1*int(self.zep.navigator.goal_position)))
#             
#         else:
#            reply = ('INFO > H:' 
#                      + str(height) 
#                      +'; GH:' 
#                      + str(goal_height) 
#                      + '; E:' + str(error) 
#                      + '; LM:' + str(left_motor) 
#                      + '; RM:' + str(right_motor) 
#                      + '; VM:' + str(vert_motor) 
#                      +  '; X:' +str(int(self.zep.navigator.position.xcoord))
#                      +'; Y:' +str(-1*int(self.zep.navigator.position.ycoord))
#                      + '; GX:' + str(int(self.zep.navigator.goal_position.xcoord))
#                      +'; GY:' +str(-1*int(self.zep.navigator.goal_position.ycoord))) 
#             
#         return reply
#     
#     def switch(self, request):
#         if self.zep.AUTO_MODE:
#             self.zep.AUTO_MODE = False
#             reply = 'SWITCH > MANUAL MODE' #If wanted, this reply can change
#             return reply
#         else:
#             self.zep.AUTO_MODE = True
#             reply = 'SWITCH > AUTOMATIC MODE'
#             return reply
#         
#     def shutdown(self, request):
#         reply = 'SHUTDOWN > SHUTTING DOWN IN 3 SECONDS'
#         return reply
#         self.zep.shutdown() #This method waits 3 seconds
#         
#     def connect(self, request):
#         reply = 'CONNECT > CONNECTION ESTABLISHED'
#         return reply
#     
#     def stabilize(self, request):
#         height = re.search('(\d+)', request)
#         self.zep.goal_height = height.group(1)
#         if height.group(1) <= 0:
#             self.zep.stabilize(False)
#             reply = 'STABILIZE > STOPPING STABILIZE'
#         else:
#             self.zep.stabilize(True)
#             reply = 'STABILIZE > STABILIZING ON: ' + str(height.group(1))
#         return reply
#     
#     def command(self, request):
#         commands = {'L' : Commands.ManualTurn(self.zep,1),
#                     'R' : Commands.ManualTurn(self.zep,-1),
#                     'S' : Commands.VertMove(100),
#                     'D' : Commands.VertMove(-100),
#                     'V' : Commands.ManualMove(1),
#                     'A' : Commands.ManualMove(-1),
#                     'STOP':Commands.Stop(self.zep)}
#         
#         reply = 'Not recognized'
#         if any(word in request for word in commands):
#             new_command = commands[word]
#             new_command.execute()
#             reply = 'Executing ' + word
#         return reply
#         #TODO: find out how to make commands better, because they aren't up to snuff right now! 
#         
#     def move_to(self,request):
#        
#         com_and_coords = request.split(":")
#         coords = com_and_coords[1].split(" ")
#         
#         self.zep.moveto(int(coords[0]),int(coords[1]),int(coords[2]))
#      
#         return "moving"
#     
# 
# 

        