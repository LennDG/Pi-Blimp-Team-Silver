'''
Created on 4-mrt.-2014

@author: Pepino
'''
import pika, time
import logging
from random import randint
logging.basicConfig()
global received
received = 0
global dictionary
dictionary = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
data = []
credentials = pika.PlainCredentials('zilver', 'zilver')
parameters = pika.ConnectionParameters('localhost', 5673, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='helloFromPC') 
channel.queue_declare(queue='helloFromPI') 


def callback(ch, method, properties, body):
    global received
    data.append(time.time())
    for i in range(0,10):
        dictionary[i]=randint(1,100)
    received += 1
    if(received == 1000):
        file = open('testdata_method2','w')
        last_r = data[0]
        for d in data:
            file.write(str(d-last_r)+'\n')
            last_r = d
        file.close()


channel.basic_consume(callback,
                      queue='helloFromPI',
                      no_ack=True)

channel.start_consuming()








