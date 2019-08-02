#!/usr/bin/python

import serial
import binascii
import struct
import time
import datetime
import math
from threading import *

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
   
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

class   Ublox(Thread):
    def __init__(self, _port = ''):
        Thread.__init__(self)
        self.port_ = _port
	self.base_ = (None, None)

    def run(self):
  	    self.readData(0)

    def readData(self, running_time = 0):
        ser = serial.Serial( port=self.port_, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
        now = datetime.datetime.now()

        receive_buffer = b''

        while True:
            receive_buffer = ser.readline(200)
            index = receive_buffer.find("$GNGGA")
            if index > 0:
                fields = receive_buffer[index:].split(',')
		if self.base_[0] is None:
                    self.base_ = float(fields[2]) / 100, float(fields[4]) / 100
                else:
                    current = float(fields[2]) / 100, float(fields[4]) / 100
                    distance =  haversine(self.base_, current)
                    print '%f,%f -> %f,%f : %f'%(self.base_[0], self.base_[1], current[0], current[1], distance)
