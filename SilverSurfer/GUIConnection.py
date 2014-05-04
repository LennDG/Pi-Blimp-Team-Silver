
import socket, threading, time
import pika, logging
class GUIConn2dot1(threading.Thread, object):
    
    def __init__(self,gui):
        threading.Thread.__init__(self)
        logging.basicConfig()
        self.gui = gui
        credentials = pika.PlainCredentials('zilver', 'zilver')
        self.parameters = pika.ConnectionParameters('localhost', 5673, '/', credentials)
#       self.parameters = pika.ConnectionParameters('localhost')
        
        not_established = True
        while(not_established):
            try:
                self.initialization_consumer()
                self.initialization_sender()
                not_established = False
            except Exception:
                not_established = True

        

    def run(self):
        thrown = False
        while True:
            try:
                if thrown == False:
                    print "pre testing consuming reinitialization"
                    thrown = True
                    raise Exception
                self.channel_consumer.start_consuming()
            except Exception:
                print "GUI consumer reinitializated"
                self.connection_consumer.close()
                self.initialization_consumer()
                
    def initialization_sender(self):
        self.connection_sender = pika.BlockingConnection( self.parameters)
        self.channel_sender = self.connection_sender.channel(channel_number=4)
        self.channel_sender.exchange_declare(exchange='server', type='topic')
                
    def initialization_consumer(self):
        
        
        #Make channel_consumer
        self.connection_consumer = pika.BlockingConnection( self.parameters)
        self.channel_consumer = self.connection_consumer.channel(channel_number=3)
        self.channel_consumer.exchange_declare(exchange='server', type='topic')

        #Create queues
        info_location = self.channel_consumer.queue_declare(queue="info-location-silver")
        self.queue_info_location = info_location.method.queue
        
        info_height = self.channel_consumer.queue_declare(queue="info-height-silver")
        self.queue_info_height = info_height.method.queue
        
        private_goal_coords =  self.channel_consumer.queue_declare(queue="private-goal-silver")
        self.queue_private_goal_coords = private_goal_coords.method.queue
        
        private_status =  self.channel_consumer.queue_declare(queue="private-status-silver")
        self.queue_private_status = private_status.method.queue
        
        private_recognized =  self.channel_consumer.queue_declare(queue="private-recognized-silver")
        self.queue_private_recognized = private_recognized.method.queue
        
        private_motors_info=  self.channel_consumer.queue_declare(queue="private-motors-info-silver")
        self.queue_private_motors_info = private_motors_info.method.queue
        
        private_pid_info=  self.channel_consumer.queue_declare(queue="private-pid-info-silver")
        self.queue_private_pid_info = private_pid_info.method.queue
        
        private_goal_coords_simulator =  self.channel_consumer.queue_declare(queue="private-goal-silver-simulator")
        self.queue_private_goal_coords_simulator = private_goal_coords_simulator.method.queue
        
        private_status_simulator =  self.channel_consumer.queue_declare(queue="private-status-silver-simulator")
        self.queue_private_status_simulator = private_status_simulator.method.queue
        
        private_recognized_simulator =  self.channel_consumer.queue_declare(queue="private-recognized-silver-simulator")
        self.queue_private_recognized_simulator = private_recognized_simulator.method.queue
        
        private_motors_info_simulator=  self.channel_consumer.queue_declare(queue="private-motors-info-silver-simulator")
        self.queue_private_motors_info_simulator = private_motors_info_simulator.method.queue
        
        private_pid_info_simulator=  self.channel_consumer.queue_declare(queue="private-pid-info-silver-simulator")
        self.queue_private_pid_info_simulator = private_pid_info_simulator.method.queue
                
                #bind the queues to keys
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_info_location,routing_key="*.info.location")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_info_height,routing_key="*.info.height")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_goal_coords,routing_key="zilver.private.goalcoords")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_status,routing_key="zilver.private.status")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_recognized,routing_key="zilver.private.recognized")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_motors_info,routing_key="zilver.private.motors")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_pid_info,routing_key="zilver.private.pid.infofromzep")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_goal_coords_simulator,routing_key="zilver_simulator.private.goalcoords")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_status_simulator,routing_key="zilver_simulator.private.status")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_recognized_simulator,routing_key="zilver_simulator.private.recognized")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_motors_info_simulator,routing_key="zilver_simulator.private.motors")
        self.channel_consumer.queue_bind(exchange='server',queue=self.queue_private_pid_info_simulator,routing_key="zilver_simulator.private.pid.infofromzep")

#        self.queue_info_location.purge()
        self.channel_consumer.basic_consume(self.callback_info_location, queue=self.queue_info_location, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_info_height, queue=self.queue_info_height, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_goal_coords, queue=self.queue_private_goal_coords, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_recognized, queue=self.queue_private_recognized, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_motors_info, queue=self.queue_private_motors_info, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_pid_info, queue=self.queue_private_pid_info, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_goal_coords_simulator, queue=self.queue_private_goal_coords_simulator, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_recognized_simulator, queue=self.queue_private_recognized_simulator, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_motors_info_simulator, queue=self.queue_private_motors_info_simulator, no_ack=True)
        self.channel_consumer.basic_consume(self.callback_private_pid_info_simulator, queue=self.queue_private_pid_info_simulator, no_ack=True)

        
#         self.queue_info_location.purge()
#         self.queue_info_height.purge()
#         self.queue_private_goal_coords.purge()
#         self.queue_private_recognized.purge()
#         self.queue_private_motors_info.purge()
        
    def callback_private_pid_info(self,ch, method, properties, body):
        params = body.split(" ")
        for parameter in params:
            p = parameter.split("=")
            self.gui.zeppelin_database.zeppelins["zilver"][p[0]]=p[1]
            
    
    def callback_private_recognized(self,ch, method, properties, body):

        result = []
        points =  body.split(";")
        for point in points:
            coords = point.split(",")
            xcoord = int(coords[0])
            ycoord = int(coords[1])
            result.append((xcoord,ycoord))
        
        self.gui.update_recognized(result)
        self.gui.print_in_textbox_decisions(str(result))
        

    def callback_private_goal_coords(self,ch, method, properties, body):
        coords = body.split(",")
        self.gui.zeppelin_database.zeppelins["zilver"]['gx']= int(float(coords[0]))
        self.gui.zeppelin_database.zeppelins["zilver"]['gy']= int(float(coords[1]))
        self.gui.zeppelin_database.zeppelins["zilver"]['Goal']= int(float(coords[2]))
        
    def callback_private_motors_info(self,ch, method, properties, body):
        coords = body.split(" ")
        self.gui.zeppelin_database.zeppelins["zilver"]['left-motor']= int(float(coords[0]))
        self.gui.zeppelin_database.zeppelins["zilver"]['right-motor']= int(float(coords[1]))
        self.gui.zeppelin_database.zeppelins["zilver"]['vert-motor']= int(float(coords[2]))
        
    def callback_private_pid_info_simulator(self,ch, method, properties, body):
        params = body.split(" ")
        print str(params)
        for parameter in params:
            p = parameter.split("=")
            self.gui.zeppelin_database.zeppelins["zilver_simulator"][p[0]]=p[1]
            
    
    def callback_private_recognized_simulator(self,ch, method, properties, body):

        result = []
        points =  body.split(";")
        for point in points:
            coords = point.split(",")
            xcoord = int(coords[0])
            ycoord = int(coords[1])
            result.append((xcoord,ycoord))
        
        self.gui.update_recognized(result)
        self.gui.print_in_textbox_decisions(str(result))
        

    def callback_private_goal_coords_simulator(self,ch, method, properties, body):
        coords = body.split(",")
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['gx']= int(float(coords[0]))
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['gy']= int(float(coords[1]))
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['Goal']= int(float(coords[2]))
        
    def callback_private_motors_info_simulator(self,ch, method, properties, body):
        coords = body.split(" ")
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['left-motor']= int(float(coords[0]))
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['right-motor']= int(float(coords[1]))
        self.gui.zeppelin_database.zeppelins["zilver_simulator"]['vert-motor']= int(float(coords[2]))
        
        
    def callback_info_location(self,ch, method, properties, body):
        zeppelin =  method.routing_key.split('.')[0]
        coor = body.split(',')
        
        if self.gui.zeppelin_database.zeppelins.has_key(zeppelin):
            self.gui.zeppelin_database.zeppelins[zeppelin]['x'] = int(float(coor[0]))
            self.gui.zeppelin_database.zeppelins[zeppelin]['y'] = int(float(coor[1]))
        else:
            self.gui.zeppelin_database.addZeppelin(zeppelin)
        
    def callback_info_height(self,ch, method, properties, body):
        zeppelin =  method.routing_key.split('.')[0]
        if self.gui.zeppelin_database.zeppelins.has_key(zeppelin):
            self.gui.zeppelin_database.zeppelins[zeppelin]['z'] = int(float(body))
        else:
            self.gui.zeppelin_database.addZeppelin(zeppelin)
        

    def send_message_to_zep(self,message,zep):
        try:
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.private.fromPC', body=message)
        except Exception:
            self.initialization_sender()
            
    def move_to(self,x,y,z,zep):
        try:
            print "move to sended"
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.hcommand.move', body=x+","+y)
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.hcommand.elevate', body=z)
        except Exception:
            self.initialization_sender()
            
    def set_motors(self,one,two,three,zep):
        try:
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.lcommand.motor1', body=one)
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.lcommand.motor2', body=two)
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.lcommand.motor3', body=three)
        except Exception:
            self.initialization_sender()
            
    def set_parameters(self,message,zep):
        try:
            self.channel_sender.basic_publish(exchange='server', routing_key=zep+'.private.pid.setpid', body=message)
            
        except Exception:
            self.initialization_sender()






                