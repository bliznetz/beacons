import re
import socket
import datetime
import subprocess
#Option text=True was added in Python 3.7. Raspberian has Python 3.5 and it's not straightforward to upgrade it
testblescan = subprocess.Popen(['cat','data.txt'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
#testblescan = subprocess.Popen(['python', 'testblescan.py'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

x=''
for line in iter(testblescan.stdout.readline,''):
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
        x = x + ' ' + t
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma


    print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='')
    x=''