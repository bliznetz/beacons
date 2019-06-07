import socket
import datetime
import subprocess
import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError
#import kafka
import logging

testblescan = subprocess.Popen(['python', 'testblescan.py'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
logger=logging.getLogger()
#producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'], value_serializer=lambda v: binascii.hexlify(v.encode)
producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'])
x=''
for line in iter(testblescan.stdout.readline,''):
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string
        x = x + ' ' + t
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    #sys.stdout.write('')
    #print topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, #For Python2
    #print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='') #For Python3
    try:
       # producer.send(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x)
       producer.send(topic,x)
       logger.info("Sent data to topic")
       print('%s sent succesfully to %s' % x topic)
    except KafkaError:
        logger.info("Can't send data to Kafka")
    x=''



#pip3 install kafka-python