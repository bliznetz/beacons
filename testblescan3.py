import re
import sys
import socket
import datetime
import blescan3
import bluetooth._bluetooth as bluez
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

kafka_server = '13.69.135.70:9092'
kafka_dev_server = '10.66.216.17:9092'
dev_id = 0

logging.basicConfig(filename="/var/log/testblescan3.log", level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%b-%d-%y %H:%M:%S')
'''
logger = logging.getLogger('iscan3')
logger.handlers = []
file_handler = logging.FileHandler('/iscan3/PyBlescan-CpToKafka/iscan3.log')
file_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%b-%d-%y %H:%M:%S')
file_handler.setFormatter(f_format)
logger.addHandler(file_handler)
#logger.info("Program started")
#logger.parent
#logger.name
'''

try:
    sock = bluez.hci_open_dev(dev_id)
    logging.info("Found Beacon")

except:
    logging.exception("Error ocured while accessing bluetooth device")
    sys.exit(1)

blescan3.hci_le_set_scan_parameters(sock)
blescan3.hci_enable_le_scan(sock)

producer = KafkaProducer(bootstrap_servers=[kafka_server], value_serializer=lambda v: v.encode('utf-8'))
producer_dev = KafkaProducer(bootstrap_servers=[kafka_dev_server], value_serializer=lambda v: v.encode('utf-8'))

x=""
while True:
    returnedList = blescan3.parse_events(sock, 5)
    for beacon in returnedList:
        for t in (beacon.split(","))[2: 9]:
            x = x + " " + t

        topic = ((re.match("^([^,]+)", beacon)).group()).replace(":", "")
        data_time = datetime.datetime.now().strftime("%s")
        value = socket.gethostname() + " " + data_time + x 
        try:
            producer.send(topic, value)
            logging.info("Location and data %s from host %s was sent to topic %s server %s" % (x, socket.gethostname(), topic, kafka_server))
            producer_dev.send(topic, value)
            logging.info("Location and data %s from host %s was sent to topic %s server %s" % (x, socket.gethostname(), topic, kafka_dev_server))
        except KafkaError:
            logging.exception("Can't send geodata %s to Kafka topic %s" % (x, topic))

        x=""
        sys.stdout.flush()
