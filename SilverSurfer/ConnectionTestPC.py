



class GUIConn2dot1(threading.Thread, object):
    
    def __init__(self,gui):
        
        threading.Thread.__init__(self)
        logging.basicConfig()
        self.gui = gui
        adress_server = '192.168.1.6'
        
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
        channel.queue_bind(exchange='server',queue=queue_private,routing_key="*.private.fromZep")
        
        channel.basic_consume(callback_info_location, queue=queue_info_loc, no_ack=True)
        channel.basic_consume(callback_info_height, queue=queue_info_height, no_ack=True)
        channel.basic_consume(callback_private, queue=queue_private, no_ack=True)
        
        
        
        

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
        self.gui.zeppelin_database.zeppelins[zeppelin]['x'] = int(coor[0])
        self.gui.zeppelin_database.zeppelins[zeppelin]['y'] = int(coor[1])
        
    def callback_info_height(self,ch, method, properties, body):
        zeppelin =  method.routing_key.split('.')[0]
        self.gui.zeppelin_database.zeppelins[zeppelin]['z'] = int(body)

    def send_message_to_zep(self,message):
        self.channel.basic_publish(exchange='server', routing_key='silversurfer.private.fromPC', body=message)






