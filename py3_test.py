import re
import socket
import datetime
import subprocess
import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError
#import kafka
import logging
import binascii

testblescan = subprocess.Popen(['python3', 'testblescan3.py'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
logger=logging.getLogger()
producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'], value_serializer=lambda v: v.encode('utf-8'))
x=''
for line in iter(testblescan.stdout.readline,''):
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
        x = x + ' ' + t
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    #sys.stdout.write('')
    #print topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, #For Python2
    #print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='') #For Python3
    try:
       # producer.send(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x)
       producer.send(topic,x)
       logger.info("Sent data to topic")
       #print('{} sent succesfully to {}'.format(x, topic))
       print("%s sent to %s" % (x, topic))
    except KafkaError:
        logger.info("Can't send data to Kafka")
        print('Can\'t send to Kafka')
    x=''



#pip3 install kafka-python