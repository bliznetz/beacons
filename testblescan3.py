import blescan3
import sys
import re
import datetime
import socket
import bluetooth._bluetooth as bluez
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
kafka_server = '10.66.216.17:9092'

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
#	print("ble thread started")

except:
	print("error accessing bluetooth device...")
	sys.exit(1)

blescan3.hci_le_set_scan_parameters(sock)
blescan3.hci_enable_le_scan(sock)

logging.basicConfig(filename="/var/log/testblescan3.log", level=logging.INFO)
producer = KafkaProducer(bootstrap_servers=[kafka_server], value_serializer=lambda v: v.encode('utf-8'))

x=''

while True:
	returnedList = blescan3.parse_events(sock, 5)
	for beacon in returnedList:
            #print(beacon)
		
            for t in (beacon.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
                x = x + ' ' + t
            topic = ((re.match('^([^,]+)', beacon)).group()).replace(':', '')  # Find first element before comma
            #print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='\n') #For Python3
            data_time = datetime.datetime.now().strftime("%s")
            value = socket.gethostname() + ' ' + data_time + x 
            try:
                producer.send(topic, value)
                logging.info("Location and data %s from host %s was sent to topic %s" % (x, socket.gethostname(), topic))
                #print("Location and data %s from host %s was sent to topic %s" % (x, socket.gethostname(), topic))
            except KafkaError:
                logger.error("Can't send geodata %s to Kafka topic %s" % (x, topic))
                #print('Can\'t send to Kafka')
            x=''
            sys.stdout.flush()
