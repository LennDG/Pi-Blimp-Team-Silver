'''
Created on 4-mrt.-2014

@author: Pepino
'''
import pika


adress_server = 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(
               adress_server))
channel = connection.channel()

channel.queue_declare(queue='hello') 



# Receiving messages from the queue is more complex. 
#It works by subscribing a callback function to a queue. 
#Whenever we receive a message, this callback function is called by the Pika library. 
#In our case this function will print on the screen the contents of the message.

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

# Next, we need to tell RabbitMQ that this particular callback function should receive messages from our hello queue:

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
