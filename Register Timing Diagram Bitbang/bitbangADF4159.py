import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

global clock, le, txData
clock = 17
le = 27
txData = 22

GPIO.setup(clock, GPIO.OUT) #Set pin to output
GPIO.output(clock, False) #Set pin to low ("False")
# Need SPI data input for thhis: GPIO.setup([data placeholder], GPIO.IN) 
GPIO.setup(le, GPIO.OUT) #Set pin to output
GPIO.output(le, False) #Set pin to low ("False")
GPIO.setup(txData, GPIO.OUT) #Set pin to output
GPIO.output(txData, False) #Set pin to low ("False")

def ADAR4159Read(reg, data, cs):
	d = list(bin(int(data, 16))[2:].zfill(8))
 
	for i in range(len(r)):
		d[i] = int(d[i])
	
	bits = [d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]]
	#response = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
	GPIO.output(clock, False)
	GPIO.output(le, True)
	
	for i in range(len(bits)):
		if bits[i] == 1:
			GPIO.output(mosi, True)
			time.sleep(0.00000000000001)
			GPIO.output(clock, True)
		if i == 4:
			time.sleep(0.000000010)
			break
		else:
			time.sleep(0.000000000001)
			response[i] = GPIO.input(miso)
			GPIO.output(clock, False)
			GPIO.output(mosi, bits[i+1])
			time.sleep(0.000000000001)
		
	GPIO.output(mosi, False)
	GPIO.output(csel, True)
	if w:
		print response
	return

def ADAR4159Write(reg, data, cs):
	return

while True:
	ADAR4159Read(1, "A", "55", 0)  

ADAR4159(0, "0", "99", 0)	
ADAR4159(0, "A", "55", 0)
ADAR4159(1, "A", "00", 0)




