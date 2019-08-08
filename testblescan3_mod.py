import blescan3
import sys
import re
import datetime
import socket
import bluetooth._bluetooth as bluez

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
#	print("ble thread started")

except:
	print("error accessing bluetooth device...")
	sys.exit(1)

blescan3.hci_le_set_scan_parameters(sock)
blescan3.hci_enable_le_scan(sock)

x=''
while True:
	returnedList = blescan3.parse_events(sock, 5)
#	print "----------"
	for beacon in returnedList:
            #print(beacon)
		
            for t in (beacon.split(','))[2: 6]:  #Split string by comma, select 3,4,5 and 6 fields and insert in into a new string.
                x = x + ' ' + t
            topic = ((re.match('^([^,]+)', beacon)).group()).replace(':', '')  # Find first element before comma
#        print(topic)
    #sys.stdout.write('')
    #print topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, #For Python2
            print(topic,socket.gethostname(),datetime.datetime.now().strftime("%s"),x, end='\n') #For Python3
            x=''
            sys.stdout.flush()
