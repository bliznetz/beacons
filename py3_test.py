import re
import socket
import datetime
from subprocess import *
import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError
#import kafka
import logging
import binascii
import testblescan3



#def blescan_to_kafka(script):

testblescan = subprocess.Popen(['python3', testblescan3], stdout=subprocess.PIPE, bufsize=1)
#universal_newlines=True)
#iter = testblescan.communicate()    
    #logger=logging.getLogger()
    #producer = KafkaProducer(bootstrap_servers=[kafka_server], value_serializer=lambda v: v.encode('utf-8'))
x=''
#for line in iter(testblescan.stdout.readline):
#for line in stdout:
   # line = testblescan.stdout.readline()
#(testblescan.stdout.readline,''):
#for line in testblescan3.returnedList:
for t in (beacon.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
        print(t)
        x = x + ' ' + t
        print(x)
topic = ((re.match('^([^,]+)', beacon)).group()).replace(':', '')  # Find first element before comma
print(topic)
x=''
    #sys.stdout.write('')
    #print topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, #For Python2
print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='') #For Python3


'''
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
'''
#blescan_to_kafka ('testblescan3.py')
# '10.66.216.17:9092')

#pip3 install kafka-python
#pip3 install pybluez
#pip3 install bitstring