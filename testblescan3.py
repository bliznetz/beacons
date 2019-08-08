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

while True:
	returnedList = blescan3.parse_events(sock, 5)
#	print "----------"
	for beacon in returnedList:
            print(beacon)
            sys.stdout.flush()		
    #sys.stdout.write('')
