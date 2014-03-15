import pika


adress_server = 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(
               adress_server))
channel = connection.channel()

channel.queue_declare(queue='helloFromPC') 
channel.queue_declare(queue='helloFromPI') 





def callback(ch, method, properties, body):
    channel.basic_publish(exchange='', routing_key='helloFromPI', body='PI sending Hello')
    


channel.basic_consume(callback,queue='helloFromPC',no_ack=True)

channel.start_consuming()



