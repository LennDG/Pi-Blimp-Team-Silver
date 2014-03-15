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
        adress_server = 'localhost'
        
        #Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel(channel_number=2)
        self.channel.exchange_declare(exchange='server', type='topic')

        #Create queues
        info_location = self.channel.queue_declare(queue="info-loc-queue-gui")
        queue_info_location = info_location.method.queue
        
        info_height = self.channel.queue_declare(queue="info-height-queue-gui")
        queue_info_height = info_height.method.queue


        hcommand_move = self.channel.queue_declare(queue="hcommand-move-queue-gui")
        queue_hcommand_move = hcommand_move.method.queue
        
        hcommand_elevate = self.channel.queue_declare(queue="hcommand-elevate-queue-gui")
        queue_hcommand_elevate = hcommand_elevate.method.queue
        
        lcommand_motor1 = self.channel.queue_declare(queue="lcommand-motor1-queue-gui")
        queue_lcommand_motor1 = lcommand_motor1.method.queue
        
        lcommand_motor2 = self.channel.queue_declare(queue="lcommand-motor2-queue-gui")
        queue_lcommand_motor2 = lcommand_motor2.method.queue
        
        lcommand_motor3 = self.channel.queue_declare(queue="lcommand-motor3-queue-gui")
        queue_lcommand_motor3 = lcommand_motor1.method.queue
        
        private =  self.channel.queue_declare(queue="private-queue-gui")
        queue_private = private.method.queue
        
        #bind the queues to keys
        self.channel.queue_bind(exchange='server',queue=queue_info_location,routing_key="*.info.location")
        self.channel.queue_bind(exchange='server',queue=queue_info_height,routing_key="*.info.height")
        self.channel.queue_bind(exchange='server',queue=queue_hcommand_elevate,routing_key="*.hcommand.elevate")
        self.channel.queue_bind(exchange='server',queue=queue_hcommand_move,routing_key="*.hcommand.move")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor1,routing_key="*.lcommand.motor1")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor2,routing_key="*.lcommand.motor2")
        self.channel.queue_bind(exchange='server',queue=queue_lcommand_motor3,routing_key="*.lcommand.motor3")
        self.channel.queue_bind(exchange='server',queue=queue_private,routing_key="*.private.fromZep")
        
        self.channel.basic_consume(self.callback_info_location, queue=queue_info_location, no_ack=True)
        self.channel.basic_consume(self.callback_info_height, queue=queue_info_height, no_ack=True)
        self.channel.basic_consume(self.callback_private, queue=queue_private, no_ack=True)
        
        
        
        

    def run(self):
            try:
                self.channel.start_consuming()
            except Exception:
                self.connection.close()           

    def callback_private(self,ch, method, properties, body):
        self.gui.inputqueue.put(body)       
        
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








                