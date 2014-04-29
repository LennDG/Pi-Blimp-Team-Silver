import pika, time


adress_server = 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(
               adress_server))
channel = connection.channel()

channel.queue_declare(queue='helloFromPC') 
channel.queue_declare(queue='helloFromPI') 





for i in range(0,1000):
    channel.basic_publish(exchange='', routing_key='helloFromPI', body='PI sending Hello')


    

    




