#This is the client conneciton side, housed on PC

import socket, threading, time
import pika, logging

class GUIConn(threading.Thread, object):
    
    def __init__(self, inqueue, outqueue):
        threading.Thread.__init__(self)

        HOST = '192.168.1.6'
        PORT = 8888
        
        self.inqueue= inqueue
        self.outqueue = outqueue
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.s.setblocking(True)
        
    def run(self):
        while True:
            try:
                time.sleep(0.5)
                data = self.outqueue.get(True) #BLOCKING CALL

                self.s.sendall(data)
                
                reply = self.s.recv(1024) #BLOCKING CALL
                print 'lol'
                print reply
                self.inqueue.put(reply)
            except Exception:
                self.s.close()
                
class GUIConn2dot0(threading.Thread, object):
    
    def __init__(self,gui):
        
        threading.Thread.__init__(self)
        logging.basicConfig()
        self.gui = gui
        adress_server = 'localhost'
        
        #Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel(channel_number=2)

        #Create Queues
        self.channel.queue_declare(queue='FromGUI')
        self.channel.queue_declare(queue='FromZEP')

        #Callback handles received messages from FromZEP
        self.channel.basic_consume(self.callback,
                      queue='FromZEP',
                      no_ack=True)
        
        
        
        
        

    def run(self):
            try:
                self.channel.start_consuming()
            except Exception:
                self.connection.close()           

    def callback(self,ch, method, properties, body):
        print body
        self.gui.inputqueue.put(body)       

    def send_message_to_zep(self,message):
        self.channel.basic_publish(exchange='', routing_key='FromGUI', body=message)
        




class GUIConn2dot1(threading.Thread, object):
    
    def __init__(self,gui):
        threading.Thread.__init__(self)
        logging.basicConfig()
        self.gui = gui
        self.initialization()
        
        

    def run(self):
        thrown = False
        while True:
            try:
                if thrown == False:
                    print "pre testing reinitialization"
                    thrown = True
                    raise Exception
                self.channel.start_consuming()
            except Exception:
                print "GUI reinitializated"
                self.connection.close()
                self.initialization()
                
    def initialization(self):
        
        adress_server = 'localhost' #'192.168.1.6'
        
        #Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel(channel_number=2)
        self.channel.exchange_declare(exchange='server', type='topic')

        #Create queues
        info_location = self.channel.queue_declare(queue="info-location-silver")
        self.queue_info_location = info_location.method.queue
        
        info_height = self.channel.queue_declare(queue="info-height-silver")
        self.queue_info_height = info_height.method.queue
        
        private_goal_coords =  self.channel.queue_declare(queue="private-goal-silver")
        self.queue_private_goal_coords = private_goal_coords.method.queue
        
        private_status =  self.channel.queue_declare(queue="private-status-silver")
        self.queue_private_status = private_status.method.queue
        
        private_recognized =  self.channel.queue_declare(queue="private-recognized-silver")
        self.queue_private_recognized = private_recognized.method.queue
                
                #bind the queues to keys
        self.channel.queue_bind(exchange='server',queue=self.queue_info_location,routing_key="*.info.location")
        self.channel.queue_bind(exchange='server',queue=self.queue_info_height,routing_key="*.info.height")
        self.channel.queue_bind(exchange='server',queue=self.queue_private_goal_coords,routing_key="silversurfer.private.goalcoords")
        self.channel.queue_bind(exchange='server',queue=self.queue_private_status,routing_key="silversurfer.private.status")
        self.channel.queue_bind(exchange='server',queue=self.queue_private_recognized,routing_key="silversurfer.private.recognized")
        
        self.channel.basic_consume(self.callback_info_location, queue=self.queue_info_location, no_ack=True)
        self.channel.basic_consume(self.callback_info_height, queue=self.queue_info_height, no_ack=True)
        self.channel.basic_consume(self.callback_private_goal_coords, queue=self.queue_private_goal_coords, no_ack=True)
        self.channel.basic_consume(self.callback_private_recognized, queue=self.queue_private_recognized, no_ack=True)
        
    
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
        self.gui.zeppelin_database.zeppelins["silversurfer"]['gx']= int(float(coords[0]))
        self.gui.zeppelin_database.zeppelins["silversurfer"]['gy']= int(float(coords[1]))
        self.gui.zeppelin_database.zeppelins["silversurfer"]['Goal']= int(float(coords[2]))
        
        
    def callback_info_location(self,ch, method, properties, body):
        zeppelin =  method.routing_key.split('.')[0]
        coor = body.split(',')
        self.gui.zeppelin_database.zeppelins[zeppelin]['x'] = int(float(coor[0]))
        self.gui.zeppelin_database.zeppelins[zeppelin]['y'] = int(float(coor[1]))
        
    def callback_info_height(self,ch, method, properties, body):
        zeppelin =  method.routing_key.split('.')[0]

        self.gui.zeppelin_database.zeppelins[zeppelin]['z'] = int(float(body))

    def send_message_to_zep(self,message):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.private.fromPC', body=message)
        
    def move_to(self,x,y,z):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.hcommand.move', body=x+","+y)
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.hcommand.elevate', body=z)

    def set_motors(self,one,two,three):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.lcommand.motor1', body=one)
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.lcommand.motor2', body=two)
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.lcommand.motor3', body=three)







                