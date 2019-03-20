import time
from math import *
import RPi.GPIO as GPIO
from bitbangADAR1000 import ADAR1000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

global stepperPins, limitPin, clock, miso, mosi, cs0, cs1, host, port, server, client, position
global TX_CH1, TX_CH2, TX_CH3, TX_CH4
global TX_CH1_I, TX_CH1_Q, TX_CH2_I, TX_CH2_Q, TX_CH3_I, TX_CH3_Q, TX_CH4_I, TX_CH4_Q

TX_CH1_I = 0x20
TX_CH1_Q = 0x21
TX_CH2_I = 0x22
TX_CH2_Q = 0x23
TX_CH3_I = 0x24
TX_CH3_Q = 0x25
TX_CH4_I = 0x26
TX_CH4_Q = 0x27 

TX_CH1 = [TX_CH1_I,TX_CH1_Q]
TX_CH2 = [TX_CH2_I,TX_CH2_Q]
TX_CH3 = [TX_CH3_I,TX_CH3_Q]
TX_CH4 = [TX_CH4_I,TX_CH4_Q]

stepperPins = [2, 3, 4, 14] # stepper motor gpio
limitPin = 15 # limit switch
clock = 17 # spi clock
miso = 18  # spi miso
mosi = 27  # spi mosi
cs0 = 22   # chip sel 0
cs1 = 23   # chip sel 1

GPIO.setup(clock, GPIO.OUT) # Set pin to output
GPIO.output(clock, False) # Set pin to low ("False")
GPIO.setup(miso, GPIO.IN)
GPIO.setup(mosi, GPIO.OUT) # Set limit switch as input
GPIO.output(mosi, False)
GPIO.setup(cs0, GPIO.OUT) # Set pin to output
GPIO.output(cs0, True)

# Initilize stepper motor
for pin in stepperPins:
    GPIO.setup(pin, GPIO.OUT) #Set pin to output
    GPIO.output(pin, False) #Set pin to low ("False")

GPIO.setup(limitPin, GPIO.IN) #Set limit switch as input

# Initilize SPI bus
GPIO.setup(clock, GPIO.OUT) 
GPIO.output(clock, False) 
GPIO.setup(miso, GPIO.IN) # miso is an inpt
GPIO.setup(mosi, GPIO.OUT) 
GPIO.output(mosi, False)
GPIO.setup(cs0, GPIO.OUT)
GPIO.output(cs0, True) # chip select lines are active low
GPIO.setup(cs1, GPIO.OUT)
GPIO.output(cs1, True)


#Each step is a list containing GPIO pins that should be set to High
stepSequence = range(0, 8)
stepSequence[0] = [stepperPins[0]]
stepSequence[1] = [stepperPins[0], stepperPins[1]]
stepSequence[2] = [stepperPins[1]]
stepSequence[3] = [stepperPins[1], stepperPins[2]]
stepSequence[4] = [stepperPins[2]]
stepSequence[5] = [stepperPins[2], stepperPins[3]]
stepSequence[6] = [stepperPins[3]]
stepSequence[7] = [stepperPins[3], stepperPins[0]]

#calcuate number of steps per degree roation
stepsPerRev = 4076 # 4076 steps / revolution
gearReduction = 5
stepsPerDegree = stepsPerRev * gearReduction / 360

sequenceNum = 0 # initilze to first step number
curpos = 0 # initilize the current rottion angle

# ADAR1000 TX Channel setup
def Init_ADAR1000():
    # Reset all registers and enable 4-wire mode
    ADAR1000(0,0x00,0x99,0)
    time.sleep(0.1)
    ADAR1000(0,0x00,0x99,1)
    time.sleep(0.1)
    
    # Set 1.8v LDO output
    ADAR1000(0,0x400,0x55,0) # LDO_TRIM_CTRL_0
    time.sleep(0.1)
    ADAR1000(0,0x400,0x55,1)
    time.sleep(0.1)

    # Set TX VM and VGA current to nominal bias
    ADAR1000(0,0x40,0x1E,0) # TX_BIAS_CURRENT_1
    time.sleep(0.1)
    ADAR1000(0,0x40,0x1E,1)
    time.sleep(0.1)

    # Set TX DRV and LNA current to nominal bias
    ADAR1000(0,0x41,0x39,0) # TX_BIAS_CURRENT_2
    time.sleep(0.1)
    ADAR1000(0,0x41,0x39,1)
    time.sleep(0.1)

    # Enables TX subcircuit (All Chanels)
    ADAR1000(0,0x37,0xFF,0) # TX_ENABLES
    time.sleep(0.1)
    ADAR1000(0,0x37,0xFF,1)
    time.sleep(0.1)

    # TX Enable
    ADAR1000(0,0x29,0x12,0) # TR_CTRL
    time.sleep(0.1)
    ADAR1000(0,0x29,0x12,1)
    time.sleep(0.1)

    # Sets phase/amplitude to ram bypass (load over SPI)
    ADAR1000(0,0x4B,0x40,0) # MEM_CTRL
    time.sleep(0.1)
    ADAR1000(0,0x4B,0x40,1)
    time.sleep(0.1)
    
    # Set TX gain to max, attn to bypass
    TX_gain = [0x1C,0x1D,0x1E,0x1F] # TX_GAIN reg ch 1, 2, 3, 4
    for ch in TX_gain:
        ADAR1000(0,ch,0x7F,0)
        time.sleep(0.1)
        ADAR1000(0,ch,0x7F,1)
        time.sleep(0.1)

# Load the TX amplitude/phase settings
def Set_TX():
    # Load phase settings
    ADAR1000(0,0x28,0x02,0)# LD_WRK_REGS
    ADAR1000(0,0x28,0x02,1)

    # Clear TX Load
    ADAR1000(0,0x28,0x00,0)
    ADAR1000(0,0x28,0x00,1)

# Calcuate the I and Q register values and set each channel
def BeamSteering(angle):
    elements = range(0,8)
    e_angle = range(0,8)
    # element # [angle, Channel, core chip]
    elements[0] = [e_angle[0], TX_CH2, 1]
    elements[1] = [e_angle[1], TX_CH2, 0]
    elements[2] = [e_angle[2], TX_CH1, 1]
    elements[3] = [e_angle[3], TX_CH1, 0]
    elements[4] = [e_angle[4], TX_CH4, 0]
    elements[5] = [e_angle[5], TX_CH4, 1]
    elements[6] = [e_angle[6], TX_CH3, 0]
    elements[7] = [e_angle[7], TX_CH3, 1]
    
    element_spacing = 0.5
    numBits = 5
    zmax = 1.00381984
    angle_const = 5*pi/180 # 5 is changable
    db_const = 10**(0/20) # 0 is changable
    
    rad = angle*pi/180 #round to 2 places
    phase_shift = element_spacing*sin(rad)*360
    
    e_angle[4] = 0.0
    for i in [5,6,7]:
        e_angle[i] = (e_angle[i-1]+phase_shift)%360
    for i in [3,2,1,0]:
        e_angle[i] = (e_angle[i+1]-phase_shift)%360

    for i in range(0,8):  
        print e_angle[i]   
        phase_rad = e_angle[i]*pi/180 #round to 2 places   
        y = (db_const/(cos(angle_const)))*sin(phase_rad)
        x = (1-tan(phase_rad)*tan(angle_const))*cos(phase_rad)
        y_= round(y/zmax,5)
        x_= round(x/zmax,5)
        
        I_bits = round(abs(x_*(2**numBits-1)),0)
        Q_bits = round(abs(y_*(2**numBits-1)),0)

        Ipol = 0
        Qpol = 0
        if (x_ >= 0):
            Ipol = 1
        if (y_ >= 0):
            Qpol = 1         
        
        I_val = I_bits+(Ipol<<5)
        Q_val = Q_bits+(Qpol<<5)
        
        ADAR1000(0,elements[i][1][0], int(I_val), elements[i][2])
        ADAR1000(0,elements[i][1][1], int(Q_val), elements[i][2])
        
    Set_TX()


for pos in (range(g_start, g_end+g_increment, g_increment)): # loop through each roation position
    for angle in (range(b_start, b_end+b_increment, b_increment)): # at each postion, loop through the beam angles
        BeamSteering(angle)
        
    curpos = Move(curpos + g_increment) # move to the next position 