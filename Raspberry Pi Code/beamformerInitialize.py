import time
import sys
import math
import subprocess
import os
import numpy as np

# ADAR1000 RX Channel setup
def Init_ADAR1000():
    ## Initializing ADAR1000 RX_1 for signal input ##
    #writeDelay = 0.01
    # Reset the whole board
    os.system('sudo ./spitest 0000 81')
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2000 81')
    #time.sleep(writeDelay)

    # Configure the whole board for SPI communication
    os.system('sudo ./spitest 0000 18')
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2000 18')
    #time.sleep(writeDelay)
    
    # Set 1.8v LDO output (Adjust LDOs) # NEED THIS TO WORK LATER
    os.system('sudo ./spitest 0400 55') # LDO_TRIM_CTRL_0
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2400 55')
    #time.sleep(writeDelay)

    # Select SPI for channel settings
    os.system('sudo ./spitest 0038 60')
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2038 60')
    #time.sleep(writeDelay)

    # Enable LNA
    os.system('sudo ./spitest 002E 7F') 
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 202E 7F')
    #time.sleep(writeDelay)

    #Set RX LNA bias to 8
    os.system('sudo ./spitest 0034 08') 
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2034 08')
    #time.sleep(writeDelay)

    #Set RX VGA bias to 2
    os.system('sudo ./spitest 0035 16') 
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2035 16')
    #time.sleep(writeDelay)

    # Enables the whole Rx 
    os.system('sudo ./spitest 0031 20') 
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2031 20')
    #time.sleep(writeDelay)

    # Loads the Rx working registers from the SPI 
    os.system('sudo ./spitest 0028 01') 
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2028 01')
    #time.sleep(writeDelay)

print "Initalizing ADAR1004..."
Init_ADAR1000()
