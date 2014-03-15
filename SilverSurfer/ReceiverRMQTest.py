'''
Created on 4-mrt.-2014

@author: Pepino
'''
import pika
import logging
logging.basicConfig()

adress_server = '192.168.1.6'

connection = pika.BlockingConnection(pika.ConnectionParameters(
               adress_server))
channel = connection.channel()

channel.queue_declare(queue='helloFromPC') 
channel.queue_declare(queue='helloFromPI') 

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    channel.basic_publish(exchange='', routing_key='helloFromPC', body='PC sending Hello')
    print "PC sending Hello"

channel.basic_publish(exchange='', routing_key='helloFromPC', body='PC sending Hello')

channel.basic_consume(callback,
                      queue='helloFromPI',
                      no_ack=True)

channel.start_consuming()






