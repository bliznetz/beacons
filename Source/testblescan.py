# Mira's revision 11/19/2018
# test BLE Scanning software
# jcs 6/8/2014

import re
import sys
import socket
import blescan
import datetime
import bluetooth._bluetooth as bluez
from kafka import KafkaProducer
from kafka.errors import KafkaError

kafka_server = '13.69.135.70:9092'
kafka_dev_server = '10.66.216.17:9092'
dev_id = 0

try:
    sock = bluez.hci_open_dev(dev_id)

except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

producer = KafkaProducer(bootstrap_servers=[kafka_server], value_serializer=lambda v: v.encode("utf-8"))
producer_dev = KafkaProducer(bootstrap_servers=[kafka_dev_server], value_serializer=lambda v: v.encode("utf-8"))

x = ""
while True:
    returnedList = blescan.parse_events(sock, 5)
    for beacon in returnedList:
        if beacon :
            print(beacon)
            for t in (beacon.split(","))[2:9]:
                x = x + " " + t

            topic = ((re.match("^([^,]+)", beacon)).group()).replace(":", "") # first element before comma is bdaddr
            print("sending to topic " + topic)
            date_time = datetime.datetime.now().strftime("%s")
            value = socket.gethostname() + ' ' + date_time + x
            try:
                producer.send(topic, value)
                producer_dev.send(topic, value)
                print("sent ok")
            except KafkaError:
                print("kafka error")
            x = ""
            sys.stdout.flush()
