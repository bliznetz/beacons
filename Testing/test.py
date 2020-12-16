import re
import socket
import datetime
import subprocess
#output = subprocess.check_output(["python", "testblescan.py"], text=True)
testblescan = subprocess.check_output(['cat','data.txt'], universal_newlines=True) #Option text=True was added in Python 3.7. Raspberian has Python 3.5 and it's not straightforward to upgrade it

x=''
for line in testblescan.split('\n'):   #Split one string into multipule
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
        x = x + t + ' '
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x)
    x=''