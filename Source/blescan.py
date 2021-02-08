# BLE iBeaconScanToKafke based on https://github.com/switchdoclabs/iBeacon-Scanner-.git
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
import struct
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

def nullParser(frame) :
    sys.stdout.write("nullBeacon: ")
    for i in frame :
        sys.stdout.write("%02X " % i)

    sys.stdout.write("\n");
    return ""

def iBeaconParser(frame) :
    num_reports = frame[0]
    for i in range(0, num_reports):
        if DEBUG == True :
            print("iBeacon")

        # fake data, all of it
        Adstring = packed_bdaddr_to_string(frame[3:9])
        Adstring += ","
        Adstring += returnstringpacket(frame[-22:-6])
        Adstring += ","
        Adstring += "%i" % returnnumberpacket(frame[-6:-4])
        Adstring += ","
        Adstring += "%i" % returnnumberpacket(frame[-4:-2])
        Adstring += ","
        Adstring += "%i" % frame[-2]
        Adstring += ","
        Adstring += "%i" % frame[-1]
        Adstring += ",76,365,7987" # Fake telemetry data

        if (DEBUG == True):
            print("\tAdstring = ", Adstring)

    return Adstring

def custBeaconParser(frame) :
    num_reports = frame[0]
    for i in range(0, num_reports):
        temperature = (frame[12] * 0x100 + frame[13])/100
        if DEBUG == True :
            print("custom beacon")

        Adstring = packed_bdaddr_to_string(frame[3:9])
        Adstring += ","
        Adstring += returnstringpacket(frame[11:16])
        Adstring += ","
        Adstring += "%i" % 10011 # fake major
        Adstring += ","
        Adstring += "%i" % 11000 # fake minor
        Adstring += ","
        Adstring += "%i" % -59 # fake rssi
        Adstring += ","
        Adstring += "%i" % -47 # fake rssi
        Adstring += ",88,"
        Adstring += "%i" % temperature
        Adstring += ",5123"

        if (DEBUG == True):
            print("\tAdstring = ", Adstring)

    return Adstring

def parse_events(sock, loop_count):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    iBeaconIdString = (255, 76, 0, 2, 21)
    # Type - xFF (255)
    # MFGID - x4C x00 (76 0)
    # Type - Proximity / iBeacon - x02 (2)
    # Length - x15 (21)

    custBeaconIdString = (255, 00, 128, 1)
    # Type - xFF (255)
    # MFGID - x00 x80 (0 128)
    # Type - x01 Bio telemetry (1)

    beaconType = 0x01

    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock. setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    done = False
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

            parser = nullParser
            if pkt[11] == beaconType and pkt[14:19]:
                if struct.unpack("BBBBB", pkt[14:19]) == iBeaconIdString :
                    parser = iBeaconParser
                elif struct.unpack("BBBB", pkt[14:18]) == custBeaconIdString :
                    parser = custBeaconParser

            if subevent == EVT_LE_CONN_COMPLETE:
                le_handle_connection_complete(pkt)
            elif ((subevent == EVT_LE_ADVERTISING_REPORT)):
                myFullList.append(parser(pkt))

    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return myFullList
