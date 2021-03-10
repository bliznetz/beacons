# BLE iBeaconScanner based on https://gitlab.com/bliznetz/ibeaconscantokafka.git
#05/24/19

# BLE iBeaconScanToKafka based on https://github.com/switchdoclabs/iBeacon-Scanner-.git
# Mira 11/19/18
#
# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14

DEBUG = False
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

import os
import sys
import codecs
import struct
import binascii
import bluetooth._bluetooth as bluez

LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04

CONSTANT_RSSI = -5

bdaddr_blacklist = [[0x15, 0xA2, 0x8A, 0x37, 0x33, 0xD4], [0xBD, 0xF2, 0xCC, 0x2E, 0xB3, 0xFD]]

def returnnumberpacket(pkt):
    myInteger = 0
    multiple = 256
    for c in pkt:
        myInteger +=  c * multiple
        multiple = 1
    return myInteger 

def returnstringpacket(pkt):
    myString = "";
    for c in pkt:
        myString +=  "%02x " % c
    return myString 

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % c)
    sys.stdout.write("\n")

def get_packed_bdaddr(bdaddr_string):
    packable_addr = []
    addr = bdaddr_string.split(':')
    addr.reverse()
    for b in addr: 
        packable_addr.append(int(b, 16))
    return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
    return ":".join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01

def bdaddr_allowed(addr) :
    for blackaddr in bdaddr_blacklist:
        match = True
        for i in range(0,6) :
            if blackaddr[i] != addr[i] :
                match = False
                break

        if match :
            return False

    return True

def clipData(data, low, high) :
    if data < low :
        return low
    elif data > high :
        return high
    else :
        return data

def nullParser(frame) :
    if (DEBUG == True) :
        sys.stdout.write("nullBeacon: ")
        for i in frame :
            sys.stdout.write("%02X " % i)

        sys.stdout.write("\n");
    return ""

def iBeaconParser(frame) :
    if True : #DEBUG == 
        printpacket(frame)
    num_reports = frame[0]
    for i in range(0, num_reports):
        heartrate = frame[19]
        temperature = (frame[21] * 0x100 + frame[20])
        stepcount = (frame[23]*0x100 + frame[22])
        if DEBUG == True :
            print("iBeacon")

        if bdaddr_allowed(frame[3:9]) :
            Adstring = packed_bdaddr_to_string(frame[3:9])
            Adstring += ","
            Adstring += returnstringpacket(frame[15:24])
            Adstring += ","
            Adstring += "%i" % returnnumberpacket(frame[-6:-4])
            Adstring += ","
            Adstring += "%i" % returnnumberpacket(frame[-4:-2])
            Adstring += ","
            Adstring += "%i" % CONSTANT_RSSI
            Adstring += ","
            Adstring += "%i" % clipData(frame[-1] - 256, -100, -1)
            Adstring += ","
            Adstring += "%i" % clipData(heartrate, 0, 255)
            Adstring += ","
            Adstring += "%i" % clipData(temperature, 320, 420)
            Adstring += ","
            Adstring += "%i" % clipData(stepcount, 0, 65535)
        else :
            if (DEBUG == True):
                print("Blacklisted bdaddr " + packed_bdaddr_to_string(frame[3:9]))
            Adstring = ""

        if (DEBUG == True):
            print("\tAdstring = ", Adstring)

    return Adstring

def custBeaconParser(frame) :
    num_reports = frame[0]
    for i in range(0, num_reports):
        heartrate = frame[18]
        temperature = (frame[20] * 0x100 + frame[19])
        stepcount = (frame[22]*0x100 + frame[21])
        if DEBUG == True :
            print("custom beacon")

        Adstring = packed_bdaddr_to_string(frame[3:9])
        Adstring += ","
        Adstring += returnstringpacket(frame[15:23])
        Adstring += ","
        Adstring += "%i" % 10011 # fake major
        Adstring += ","
        Adstring += "%i" % 11000 # fake minor
        Adstring += ","
        Adstring += "%i" % CONSTANT_RSSI
        Adstring += ","
        Adstring += "%i" % clipData(frame[-1] - 256, -100, -1)
        Adstring += ","
        Adstring += "%i" % clipData(heartrate, 0, 255)
        Adstring += ","
        Adstring += "%i" % clipData(temperature, 320, 420)
        Adstring += ","
        Adstring += "%i" % clipData(stepcount, 0, 65535)

        if (DEBUG == True):
            print("\tAdstring = ", Adstring)

    return Adstring

def TempTrackParser(frame) :
    if True : #DEBUG == 
        printpacket(frame)
    num_reports = frame[0]
    for i in range(0, num_reports):
        heartrate = 10 # Fake
        temperature = frame[25]*10 + (int)(frame[26]/10)
        stepcount = 10 # Fake
        if DEBUG == True :
            #
            print("TempTracker")
            for i in frame :
                sys.stdout.write("%02X " % i)
            sys.stdout.write("\n");
    
        Adstring = packed_bdaddr_to_string(frame[3:9])
        Adstring += ","
        Adstring += returnstringpacket(frame[15:24])
        Adstring += ","
        Adstring += "%i" % returnnumberpacket(frame[28:30])
        Adstring += ","
        Adstring += "%i" % returnnumberpacket(frame[30:32])
        Adstring += ","
        Adstring += "%i" % CONSTANT_RSSI
        Adstring += ","
        Adstring += "%i" % clipData(frame[-1] - 256, -100, -1)
        Adstring += ","
        Adstring += "%i" % clipData(heartrate, 0, 255)
        Adstring += ","
        Adstring += "%i" % clipData(temperature, 320, 420)
        Adstring += ","
        Adstring += "%i" % clipData(stepcount, 0, 65535)

        if (DEBUG == True): 
            print("\tAdstring = ", Adstring)

    return Adstring

def parse_events(sock, loop_count):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    
    iBeaconIdString = (255, 76, 0, 2, 21)
    # Type - xFF (255)
    # MFGID - x4C x00 (76 0)
    # Type - Proximity / iBeacon - x02 (2)
    # Length - x15 (21)

    custBeaconIdString = (255, 00, 128, 1)
    # Type - xFF (255)
    # MFGID - x00 x80 (0 128)
    # Type - x01 Bio telemetry (1)

    TempTrackIdString = (109, 112, 116, 114)
    # Type - x6D (109)
    # MFGID - x7A x74 (112 116)
    # Type  - x72 (114)

    beaconType = 0x01

    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    results = []
    myFullList = []
    for i in range(0, loop_count):
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if (DEBUG == True):
            print("------ptype, event, plen--------", ptype, event, plen)
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            i = 0
        elif event == bluez.EVT_NUM_COMP_PKTS:
            i = 0 
        elif event == bluez.EVT_DISCONN_COMPLETE:
            i = 0
        elif event == LE_META_EVENT:
            subevent = pkt[3]
            pkt = pkt[4:]

            if len(pkt) < 20 :
                continue

            parser = nullParser
            
            if struct.unpack("BBBBB", pkt[14:19]) == iBeaconIdString :
                parser = iBeaconParser
            elif struct.unpack("BBBB", pkt[14:18]) == custBeaconIdString :
                parser = custBeaconParser
            elif struct.unpack("BBBB", pkt[14:18]) == TempTrackIdString :
                parser = TempTrackParser

            if subevent == EVT_LE_CONN_COMPLETE:
                le_handle_connection_complete(pkt)
            elif subevent == EVT_LE_ADVERTISING_REPORT :
                myFullList.append(parser(pkt))

    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return myFullList
