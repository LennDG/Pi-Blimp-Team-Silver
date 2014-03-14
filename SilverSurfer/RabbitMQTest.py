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

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Wa make')
print " [x] Sent 'Wa Make'"

connection.close()

