import re
import socket
import datetime
import subprocess
output = subprocess.check_output(["python", "testblescan.py"]).decode("utf-8")

testblescan='e1:dc:ab:d3:93:01,0112233445566778899aabbccddeeff0,10011,10003,-59,-62'
topic = ((re.match('^([^,]+)', testblescan)).group()).replace(':', '') #Find first element befoe comma

#print(topic)

x=''
for i in (testblescan.split(','))[2:6]: #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
    x = x + i + ' '
#print(x)


#print(socket.gethostname())
#print(datetime.datetime.now().strftime("%s"))


print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x)

'''
for i in first_par:
    #print(i)
    #print(type(i))
    if i == (re.search(':', first_par)).group(0):
        continue
    else:
        topic = topic + i
        #print(i)
        #print(topic)
print(topic)
'''