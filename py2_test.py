#Version for Python2
import re
import socket
import datetime
import subprocess
import sys

testblescan = subprocess.Popen(['python', 'testblescan.py'], stdout=subprocess.PIPE, bufsize=1, univers$

x=''
for line in iter(testblescan.stdout.readline,''):
    for t in (line.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in $
        x = x + ' ' + t 
    topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    sys.stdout.write('')
    print topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x,
    x=''

