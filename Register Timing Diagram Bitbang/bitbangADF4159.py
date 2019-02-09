import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

global clock, le, txData
clock = 17
le = 27
txData = 22
data = 18
muxOut = 23

GPIO.setup(clock, GPIO.OUT) # Set pin to output
GPIO.output(clock, False) # Set pin to low ("False")
GPIO.setup(muxOut, GPIO.IN) # Set pin to input
GPIO.setup(le, GPIO.OUT) # Set pin to output
GPIO.output(le, True) # Set pin to high ("True")
GPIO.setup(txData, GPIO.OUT) # Set pin to output
GPIO.output(txData, False) # Set pin to low ("False")
GPIO.setup(data, GPIO.OUT) # Set pin to output
GPIO.output(data, False) # Set pin to low ("False")

def ADF4159Read(reg, data):
	d = list(bin(int(data, 16))[2:].zfill(4))
 
	for i in range(len(r)):
		d[i] = int(d[i])
	
	bits = [d[0],d[1],d[2],d[3]]
	response = [0,0,0,0]
        
	GPIO.output(clock, False)
	GPIO.output(le, True)

    GPIO.output(txData, True)
    time.sleep(0.000000020) # Note: Add time for the frequency of the phase frequency detector (PFD)
    GPIO.output(txData, False)
    time.sleep(0.00000000000001)
    GPIO.output(clock, True)
	time.sleep(0.000000020)
    GPIO.output(clock, False)

	for i in range(len(bits)):
		if bits[i] == 1:
            time.sleep(0.000000025)
			GPIO.output(clock, True)

        time.sleep(0.000000025)
        response[i] = GPIO.input(muxOut)

		if i == 3:
			time.sleep(0.000000010)
            GPIO.output(clock, False)
            GPIO.output(le, False)
			break
        else:
            GPIO.output(clock, False)
            time.sleep(0.000000000001)
		
	GPIO.output(le, False)
	print response
	return

def ADF4159Write(reg, data):
	d = list(bin(int(data, 16))[2:].zfill(4))
 
	for i in range(len(r)):
		d[i] = int(d[i])
	
	bits = [d[0],d[1],d[2],d[3]]
	response = [0,0,0,0,0]
        
	GPIO.output(clock, False)
    GPIO.output(le, True)
    time.sleep(0.00000000000001)

	GPIO.output(le, False)
    time.sleep(0.000000020) 
    GPIO.output(clock, True)
    time.sleep(0.000000025)
    GPIO.output(clock, False)

	for i in range(len(bits)):
		if bits[i] == 1:
            GPIO.output(data, True)
            time.sleep(0.000000025)
			GPIO.output(clock, True)

        time.sleep(0.000000000001)
        response[i] = GPIO.input(muxOut)

		if i == 3:
			time.sleep(0.000000010)
            GPIO.output(le, True)
            time.sleep(0.000000015)
            GPIO.output(clock, False)
            time.sleep(0.00000005)
            GPIO.output(le, False)
			break 
        else:
            time.sleep(0.000000025)
            GPIO.output(clock, False)
            GPIO.output(data, bits[i+1])
            time.sleep(0.000000000001)
		
	GPIO.output(le, False)
	print response
	return

while True:
	ADF4159Read("A", "55")  

# while True:
# 	ADF4159Write("A", "55")  

ADF4159Read("0", "9")	
ADF4159Read("A", "5")
ADF4159Write("A", "0")




