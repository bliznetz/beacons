import blescan3
import sys
import re
import datetime
import socket
import bluetooth._bluetooth as bluez
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
#	print("ble thread started")

except:
	print("error accessing bluetooth device...")
	sys.exit(1)

blescan3.hci_le_set_scan_parameters(sock)
blescan3.hci_enable_le_scan(sock)

logger=logging.getLogger()
producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'], value_serializer=lambda v: v.encode('utf-8'))

x=''
while True:
	returnedList = blescan3.parse_events(sock, 5)
#	print "----------"
	for beacon in returnedList:
            #print(beacon)
		
            for t in (beacon.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
                x = x + ' ' + t
            topic = ((re.match('^([^,]+)', beacon)).group()).replace(':', '')  # Find first element before comma
            #print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='\n') #For Python3
            try:
                #producer.send(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x)
                producer.send(topic,x)
                logger.info("Sent data to topic")
                #print('{} sent succesfully to {}'.format(x, topic))
                print("%s sent to %s" % (x, topic))
            except KafkaError:
                logger.info("Can't send data to Kafka")
                print('Can\'t send to Kafka')
            x=''
            sys.stdout.flush()
