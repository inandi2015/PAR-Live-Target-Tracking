import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

global clock, miso, mosi, cs0, cs1
clock = 17
miso = 18
mosi = 27
cs0 = 22

GPIO.setup(clock, GPIO.OUT) # Set pin to output
GPIO.output(clock, False) # Set pin to low ("False")
GPIO.setup(miso, GPIO.IN)
GPIO.setup(mosi, GPIO.OUT) # Set limit switch as input
GPIO.output(mosi, False)
GPIO.setup(cs0, GPIO.OUT) # Set pin to output
GPIO.output(cs0, True)

def ADAR1000(rw, reg, data, cs):
	w = int(rw)
	r = list(bin(int(reg, 16))[2:].zfill(8))
	d = list(bin(int(data, 16))[2:].zfill(8))

	if (cs==0):
	    csel = cs0
	else:
	    csel = cs1

          
	for i in range(len(r)):
		r[i] = int(r[i])
		d[i] = int(d[i])
	
	bits = [w,0,0,0,0,0,0,0,r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]]
	response = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
	GPIO.output(csel, True)
	GPIO.output(clock, True)
	time.sleep(0.000000010)
	GPIO.output(csel, False)
	time.sleep(0.000000010)
	GPIO.output(clock, False)
	
	for i in range(len(bits)):
		if bits[i] == 1:
			GPIO.output(mosi, True)
			time.sleep(0.00000000000001)
			GPIO.output(clock, True)

		time.sleep(0.000000000001)
		response[i] = GPIO.input(miso)
		
		if i == 23:
			time.sleep(0.000000010)
			break
		else:
			GPIO.output(clock, False)
			GPIO.output(mosi, bits[i+1])
			time.sleep(0.000000000001)
		
	GPIO.output(mosi, False)
	GPIO.output(csel, True)
	if w:
		print response
	return

# Tester: 
# while True:
# 	ADAR1000(1, "A", "55", 0)  

ADAR1000(0, "0", "99", 0)	
ADAR1000(0, "A", "55", 0)
ADAR1000(1, "A", "00", 0)




