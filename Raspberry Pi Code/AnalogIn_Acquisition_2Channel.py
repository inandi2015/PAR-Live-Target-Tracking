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
import math
import time
#import matplotlib.pyplot as plt
import sys
import numpy

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
hdwf = c_int()
sts = c_byte()
rgdSamples1 = (c_double*4000)()
rgdSamples2 = (c_double*4000)()
#print DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print "DWF Version: "+version.value

#open device
print "Opening first device"
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print szerr.value
    print "failed to open device"
    quit()

print "Preparing to read sample..."

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(40000000.0))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(4000)) 
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(5))
#wait at least 2 seconds for the offset to stabilize
time.sleep(5)

#begin acquisition
dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(True))
print "   waiting to finish"

while True:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    print "STS VAL: " + str(sts.value) + "STS DONE: " + str(DwfStateDone.value)
    if sts.value == DwfStateDone.value :
        break
    time.sleep(0.1)
print "Acquisition finished"

dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples1, 4000)
dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples2, 4000)
dwf.FDwfDeviceCloseAll()

#plot window
dc1 = sum(rgdSamples1)/len(rgdSamples1)
print "DC: "+str(dc1)+"V"

dc2 = sum(rgdSamples2)/len(rgdSamples2)
print "DC: "+str(dc2)+"V"

rgpy1=[0.0]*len(rgdSamples1)
for i in range(0,len(rgpy1)):
    rgpy1[i]=rgdSamples1[i]


rgpy2=[0.0]*len(rgdSamples2)
for i in range(0,len(rgpy2)):
   rgpy2[i]=rgdSamples2[i]

array1 = numpy.asarray(rgpy1)
numpy.savetxt("testCH1.csv", array1, delimiter=",")

array2 = numpy.asarray(rgpy2)
numpy.savetxt("testCH2.csv", array2, delimiter=",")

#plt.plot(rgpy1)
#plt.plot(rgpy2)
#plt.show()


