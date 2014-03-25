import pika
import logging

logging.basicConfig()
credentials = pika.PlainCredentials('zilver', 'zilver')
parameters = pika.ConnectionParameters('localhost',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print " [x] Sent 'Hello World!'"
connection.close()

