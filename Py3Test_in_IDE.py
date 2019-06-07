import re
import socket
import datetime
import subprocess
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
#Option 'text=True' was added in Python 3.7. Raspberian has Python 3.5 and it's not straightforward to upgrade it
testblescan = subprocess.Popen(['cat','data.txt'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
#testblescan = subprocess.Popen(['python', 'testblescan.py'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

logger=logging.getLogger()
x=''
#producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'])
for line in iter(testblescan.stdout.readline,''):
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3, 4, 5 and 6 fields and insert it into a new string.
        x = x + ' ' + t
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    #try:
     #   producer.send(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='')
    #except KafkaError:
    #    logger.info("Can't send data to Kafka")

    print(topic, socket.gethostname(), datetime.datetime.now().strftime("%s"), x, end='')
    x=''
