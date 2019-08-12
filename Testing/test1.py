import re
import socket
import datetime
import subprocess
#output = subprocess.check_output(["python", "testblescan.py"], text=True)
#testblescan = subprocess.check_output(['cat','data.txt'], universal_newlines=True) #Option text=True was added in Python 3.7. Raspberian has Python 3.5 and it's not straightforward to upgrade it
testblescan = subprocess.Popen(['cat','data.txt'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
print(testblescan)


for line in iter(testblescan.stdout.readline,''):
    print(line.rstrip())

    #topic = ((re.match('^([^,]+)', line)).group()).replace(':', '')  # Find first element before comma
    #print(type(topic))
    #print(topic)
