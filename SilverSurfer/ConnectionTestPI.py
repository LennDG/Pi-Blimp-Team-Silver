




class PiConn2dot1( threading.Thread, object):
    
    def __init__(self,gate):
        
        threading.Thread.__init__(self)
        self.gate = gate
        adress_server = 'localhost'
        
###########
#Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel()
        channel.exchange_declare(exchange='server', type='topic')

        #Create queues
        info_location = channel.queue_declare(exclusive=True,queue="info-loc-queue")
        queue_info_loc = info_location.method.queue
        
        info_height = channel.queue_declare(exclusive=True,queue="info-height-queue")
        queue_info_height = info_height.method.queue


        hcommand_move = channel.queue_declare(exclusive=True,queue="hcommand-move-queue")
        queue_hcommand_move = hcommand_move.method.queue
        
        hcommand_elevate = channel.queue_declare(exclusive=True,queue="hcommand-elevate-queue")
        queue_hcommand_elevate = hcommand_elevate.method.queue
        
        lcommand_motor1 = channel.queue_declare(exclusive=True,queue="lcommand-motor1-queue")
        queue_lcommand_motor1 = lcommand_motor1.method.queue
        
        lcommand_motor2 = channel.queue_declare(exclusive=True,queue="lcommand-motor2-queue")
        queue_lcommand_motor2 = lcommand_motor2.method.queue
        
        lcommand_motor3 = channel.queue_declare(exclusive=True,queue="lcommand-motor3-queue")
        queue_lcommand_motor3 = lcommand_motor1.method.queue
        
        private =  channel.queue_declare(exclusive=True,queue="private-queue")
        queue_private = private.method.queue
        
        #bind the queues to keys
        channel.queue_bind(exchange='server',queue=queue_info_location,routing_key="*.info.location")
        channel.queue_bind(exchange='server',queue=queue_info_height,routing_key="*.info.height")
        channel.queue_bind(exchange='server',queue=queue_hcommand_elevate,routing_key="*.hcommand.elevate")
        channel.queue_bind(exchange='server',queue=queue_hcommand_move,routing_key="*.hcommand.move")
        channel.queue_bind(exchange='server',queue=queue_lcommand_motor1,routing_key="*.lcommand.motor1")
        channel.queue_bind(exchange='server',queue=queue_lcommand_motor2,routing_key="*.lcommand.motor2")
        channel.queue_bind(exchange='server',queue=queue_lcommand_motor3,routing_key="*.lcommand.motor3")
        channel.queue_bind(exchange='server',queue=queue_private,routing_key="*.private.FromPC")
        
        channel.basic_consume(callback_hcommand_elevate, queue=queue_hcommand_elevate, no_ack=True)
        channel.basic_consume(callback_hcommand_move, queue=queue_hcommand_move, no_ack=True)
        channel.basic_consume(callback_private, queue=queue_private, no_ack=True)
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
        self.gate.elevate(body)   

    def callback_hcommand_move(self,ch, method, properties, body):
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
            self.update_server()
    
    def update_server(self):
        self.PIconnection.send_position_to_server(self.zep.navigator.position.xcoord,
                                                   self.zep.navigator.position.ycoord,
                                                    self.zep.navigator.height)
        self.PIconnection.send_message_to_gui(message)   
    
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