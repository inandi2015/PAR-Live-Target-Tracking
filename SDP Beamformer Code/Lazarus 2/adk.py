"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision: 10/17/2013

   Requires:                       
       Python 2.7, numpy, matplotlib
       python-dateutil, pyparsing
"""
from ctypes import *
from dwfconstants import *
import time
import sys
from scipy.fftpack import fft


def acquire():
    #Refer to Waveforms SDK Sample - AnalogIn_Acquisition.py
    dwf = cdll.dwf

    #declare ctype variables
    hdwf = c_int()
    sts = c_byte()
    ch1Samples = (c_double*4000)()
    ch2Samples = (c_double*4000)()

    #open device
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    #Check if device is open
    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print szerr.value
        print "failed to open device"
        quit()

    #set up acquisition for ADK
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(2000000000.0))    #Set sample frequency
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(4000)) 

    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))     #Turns on Channel 1
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(10))      #Sets the range for Channel 1

    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))     #Turns on Channel 2
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(10))      #Sets the range for Channel 2

    #wait at least 2 seconds for the offset to stabilize
    time.sleep(3)

    #begin acquisition
    dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(True))

    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    #end acquisition

    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), ch1Samples, 4000)   #Grab 4000 samples from Channel 1
    dwf.FDwfAnalogInStatusData(hdwf, c_int(1), ch2Samples, 4000)   #Grab 4000 samples from Channel 2

    file1 = open("ch1Samples.txt", 'w')
    ch1Samples_list = [0.0]*len(ch1Samples)
    
    maximum1 = 0
    for i in range(0, len(ch1Samples_list)):
        ch1Samples_list[i] = ch1Samples[i]

        if ch1Samples_list[i] > maximum1:
            maximum1 = ch1Samples_list[i]
    file1.write(str(maximum1)) 

    file2 = open("ch2Samples.txt", 'w')
    ch2Samples_list = [0.0]*len(ch2Samples)

    maximum2 = 0
    for i in range(0, len(ch2Samples_list)):
        ch2Samples_list[i] = ch2Samples[i]

        if ch2Samples_list[i] > maximum2:
            maximum2 = ch2Samples_list[i]

    file2.write(str(maximum2))

    dwf.FDwfDeviceCloseAll()
    
