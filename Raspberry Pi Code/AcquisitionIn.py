from ctypes import *
from dwfconstants import *
import math
import time
#import matplotlib.pyplot as plt
import sys
import numpy 
from numpy.fft import fft,fftfreq, ifft

class DevNull:
        def write(self, msg):
                    pass

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
hdwf = c_int()
sts = c_byte()
Length = c_double()
Min=c_int()
Max=c_int()
rgdSamples1 = (c_double*8192)()
rgdSamples2 = (c_double*8192)()
n=8192

freqs=100.0*fftfreq(n)

mask=freqs>0

dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print "szerr.value"
    print "failed to open device"
    quit()


#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(100000000.0))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(8192)) 
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(5))
#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

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

dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples1, 8192)
dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples2, 8192)
dwf.FDwfAnalogInRecordLengthSet(hdwf, byref(Length))
dwf.FDwfAnalogInBufferSizeInfo(hdwf, byref(Min), byref(Max))

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

fft_vals1=fft(rgpy1)
#fft_vals2=fft(rgpy2)

fft_theo1=2.0*numpy.abs(fft_vals1/n)
sys.stderr = DevNull()
print max(fft_theo1[mask].tolist())
sys.stderr = DevNull()
# dwf.FDwfAnalogInRecordLengthGet(hdwf, byref(Length))
# dwf.FDwfAnalogInFrequencyInfo(hdwf, byref(Min), byref(Max))

#print Min
#print Max
#print Length

#plt.figure(1)
#plt.plot(rgpy1)
#plt.plot(rgpy2)

#plt.figure(2)
#plt.plot(freqs[mask],fft_theo1[mask])
#plt.plot(freqs,fft_vals2)
#plt.show()

#fft_theo[mask].tolist()
#print max(fft_theo1[mask].tolist())
