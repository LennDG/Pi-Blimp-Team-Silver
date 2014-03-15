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
        adress_server = '192.168.1.6'
        
        #Make channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( adress_server))
        self.channel = self.connection.channel()

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
        


                