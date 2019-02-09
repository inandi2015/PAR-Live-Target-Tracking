import dwf

version = dwf.FDwfGetVersion();
print("DWF version: " + version);
hwdf = dwf.FDwfDeviceOpen()
print("HDWF" + str(hwdf))