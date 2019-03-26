#***************************  S T E E R *********************************
#
#   PURPOSE: This function steers the 2 beamforming chips to a desired angle
#            and calculates the neccesary phase shift for each antenna. All
#            values are approximated to be close to the values listed in the
#            table of phase settings
#   
#   INPUT : angle - The direction we are steering at
#           mySDP - the SDP board we are writing to
#
#
#***************************************************************************
import SDP_driver_new
import numpy as np
import fitz
import time
import lazarus
import adk
import thread

def setCourse(mySdp, angle):
    steer(mySdp, angle)
    lazarus.rise()
    target = (fitz.sweepGrab())
    lazarus.kill()
    print 'Power at '+ str(angle) + ' degrees is ' + str(target) 
    fitz.plot(angle)

def setCourse1(mySdp, angle):
    steer(mySdp, angle)
    adk.acquire()
    target = fitz.sweepGrab1()
    print 'Power at '+ str(angle) + ' degrees is ' + str(target) 
    fitz.plot(angle)


def sweep1(mySdp):
    target = []
    #Scan from 10 degrees to 180 degrees in increments of 10 degrees
    for angle in range (-40, 40, 10):
        steer(mySdp, angle)
        adk.acquire()
        target.append(fitz.sweepGrab1())
    loc = np.argmax(target)
    print loc

    #location mapping
    if loc == 0:
        loc = 13
    elif loc == 1:
        loc = 12
    elif loc == 2:
        loc = 11
    elif loc == 3:
        loc = 10
    elif loc == 4:
        loc = 9
    elif loc == 5:
        loc = 8
    elif loc == 6:
        loc = 7
    elif loc == 7:
        loc = 6
    elif loc == 8:
        loc = 5
    elif loc == 9:
        loc = 4

    print 'Possible Target found at '+ str(loc*10) + ' degrees'
    fitz.plot(loc*10)

def sweep(mySdp):
    target = [0]
    #Scan from 10 degrees to 180 degrees in increments of 10 degrees
    for angle in range (-40, 40, 10):
        steer(mySdp, angle)
        lazarus.rise()
        target.append(fitz.sweepGrab())
        lazarus.kill()
    loc = np.argmax(target)
    print 'Possible Target found at '+ str(loc*10) + ' degrees'
    fitz.plot(loc*10)

def conScan(mySdp):
    Trigger = []
    thread.start_new_thread(input_thread, (Trigger,))
    while 1:
        if Trigger: break
        for angle in range (-40, 40, 10):
            steer(mySdp, angle)
        time.sleep(1)
        for angle in range (40, -40, -10):
            steer(mySdp, angle)
        time.sleep(1)

def input_thread(Trigger):
    raw_input()
    Trigger.append(None)

#********************* T a b l e   o f  P h a s e  S e t t i n g s ************
angle_array = [0, 2.813, 5.625, 8.438, 11.25, 14.063, 16.875, 19.688, 22.5, 25.313, 28.125, 30.938, 33.75, 36.563, 39.375, 42.188, 45, 47.813, 50.625, 53.438, 56.25, 59.063, 61.875, 64.688, 67.5, 70.313, 73.125, 75.938, 78.75, 81.563, 84.375, 87.188, 90, 92.813, 95.625, 98.438, 101.25, 104.063, 106.875, 109.688, 112.5, 115.313, 118.125, 120.938, 123.75, 126.563, 129.375, 132.188, 135, 137.813, 140.625, 143.438, 146.25, 149.063, 151.875, 154.688, 157.5, 160.313, 163.125, 165.938, 168.75, 171.563, 174.375, 177.188, 180, 182.813, 185.625, 188.438, 191.25, 194.063, 196.875, 199.688, 202.5, 205.313, 208.125, 210.938, 213.75, 216.563, 219.375, 222.188, 225, 227.813, 230.625, 233.438, 236.25, 239.063, 241.875, 244.688, 247.5, 250.313, 253.125, 255.938, 258.75, 261.563, 264.375, 267.188, 270, 272.813, 275.625, 278.438, 281.25, 284.063, 286.875, 289.688, 292.5, 295.313, 298.125, 300.938, 303.75, 306.563, 309.375, 312.188, 315, 317.813, 320.625, 323.438, 326.25, 329.063, 331.875, 334.688, 337.5, 340.313, 343.125, 345.938, 348.75, 351.563, 354.375, 357.188]
I_array = [0x3F, 0x3F, 0x3F, 0x3F, 0x3F, 0x3E, 0x3E, 0x3D, 0x3D, 0x3C, 0x3C, 0x3B, 0x3A, 0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x30, 0x2F, 0x2E, 0x2C, 0x2B, 0x2A, 0x28, 0x27, 0x25, 0x24, 0x22, 0x21, 0x1, 0x3, 0x4, 0x6, 0x7, 0x8, 0xA, 0xB, 0xD, 0xE, 0xF, 0x11, 0x12, 0x13, 0x14, 0x16, 0x17, 0x18, 0x19, 0x19, 0x1A, 0x1B, 0x1C, 0x1C, 0x1D, 0x1E, 0x1E, 0x1E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1E, 0x1E, 0x1D, 0x1D, 0x1C, 0x1C, 0x1B, 0x1A, 0x19, 0x18, 0x17, 0x16, 0x15, 0x14, 0x13, 0x12, 0x10, 0xF, 0xE, 0xC, 0xB, 0xA, 0x8, 0x7, 0x5, 0x4, 0x2, 0x1, 0x21, 0x23, 0x24, 0x26, 0x27, 0x28, 0x2A, 0x2B, 0x2D, 0x2E, 0x2F, 0x31, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x39, 0x39, 0x3A, 0x3B, 0x3C, 0x3C, 0x3D, 0x3E, 0x3E, 0x3E, 0x3F, 0x3F, 0x3F]
Q_array = [0x20, 0x21, 0x23, 0x24, 0x26, 0x27, 0x28, 0x2A, 0x2B, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x38, 0x39, 0x3A, 0x3A, 0x3B, 0x3C, 0x3C, 0x3C, 0x3D, 0x3D, 0x3D, 0x3D, 0x3D, 0x3D, 0x3D, 0x3D, 0x3D, 0x3C, 0x3C, 0x3C, 0x3B, 0x3A, 0x3A, 0x39, 0x38, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x31, 0x30, 0x2F, 0x2E, 0x2D, 0x2B, 0x2A, 0x28, 0x27, 0x26, 0x24, 0x23, 0x21, 0x20, 0x1, 0x3, 0x4, 0x6, 0x7, 0x8, 0xA, 0xB, 0xD, 0xE, 0xF, 0x10, 0x11, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x18, 0x19, 0x1A, 0x1A, 0x1B, 0x1C, 0x1C, 0x1C, 0x1D, 0x1D, 0x1D, 0x1D, 0x1D, 0x1D, 0x1D, 0x1D, 0x1D, 0x1C, 0x1C, 0x1C, 0x1B, 0x1A, 0x1A, 0x19, 0x18, 0x18, 0x17, 0x16, 0x15, 0x14, 0x13, 0x11, 0x10, 0xF, 0xE, 0xD, 0xB, 0xA, 0x8, 0x7, 0x6, 0x4, 0x3, 0x1]

def steer(mySdp, angle):
    #Calculate phase shift between two elements
    pshift = fitz.phaseShift(angle) 
    #print "angle "+ str(angle) +"\tpshift: " + str(pshift)
    #Copy list of angles into a numerical python array
    phases = np.asarray(angle_array)
    plane = 360
    
    #****************** B o a r d A - RX_1  **************** 
    # 
    #Set the first antenna to 0 degrees    
    
    #//////////////////////////////////////////////////
    index = (np.abs(phases-angle)).argmin()
    
    mySdp.write_spi(0x0010, 0xFF)               #Ch1_RX_GAIN
    mySdp.write_spi(0x0014, I_array[index])     #CH1_RX_PHASE_I
    mySdp.write_spi(0x0015, Q_array[index])     #CH1_RX_PHASE_Q
    mySdp.write_spi(0x0028, 0x01)               #Load Work Registers


    #mySdp.write_spi(0x0010, 0xFF)            #Ch1_RX_GAIN
    #mySdp.write_spi(0x0014, 0X3F)            #CH1_RX_PHASE_I
    #mySdp.write_spi(0x0015, 0X20)            #CH1_RX_PHASE_Q
    #mySdp.write_spi(0x0028, 0x01)            #Load Work Registers


    #****************** B o a r d A - RX_2  **************** 
    
    #Map the angle to a value between 0 and 360 degrees
    aE2Shift = pshift % plane   
    index = (np.abs(phases-aE2Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(aE2Shift)+'\t'+str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers 
    mySdp.write_spi(0x0011, 0xff)                #Ch2_RX_GAIN
    mySdp.write_spi(0x0016, I_array[index])    #CH2_RX_PHASE_I
    mySdp.write_spi(0x0017, Q_array[index])    #CH2_RX_PHASE_Q
    mySdp.write_spi(0x0028, 0x01)                #Load Work Registers

    

    #****************** B o a r d A - RX_3  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    aE3Shift = (2 * pshift) % plane
    index = (np.abs(phases-aE3Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(aE3Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    mySdp.write_spi(0x0012, 0xff)                #Ch3_RX_GAIN
    mySdp.write_spi(0x0018, I_array[index])    #CH3_RX_PHASE_I
    mySdp.write_spi(0x0019, Q_array[index])    #CH3_RX_PHASE_Q
    mySdp.write_spi(0x0028, 0x01)                #Load Work Registers

    #****************** B o a r d A - RX_4  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    aE4Shift = (3 * pshift) % plane
    index = (np.abs(phases-aE4Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(aE4Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 

    mySdp.write_spi(0x0013, 0xff)                #Ch4_RX_GAIN
    mySdp.write_spi(0x001A, I_array[index])    #CH4_RX_PHASE_I
    mySdp.write_spi(0x001B, Q_array[index])    #CH4_RX_PHASE_Q
    mySdp.write_spi(0x0028, 0x01)                #Load Work Registers


    #****************** B o a r d B - RX_1  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    bE1Shift = (4 * pshift) % plane
    index = (np.abs(phases-bE1Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(bE1Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 

    mySdp.write_spi(0x2010, 0xff)                #Ch5_RX_GAIN
    mySdp.write_spi(0x2014, I_array[index])    #CH5_RX_PHASE_I
    mySdp.write_spi(0x2015, Q_array[index])    #CH5_RX_PHASE_Q
    mySdp.write_spi(0x2028, 0x01)                #Load Work Registers


    #****************** B o a r d B - RX_2  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    bE2Shift = (5 * pshift) % plane
    index = (np.abs(phases-bE2Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(bE2Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 

    mySdp.write_spi(0x2011, 0xff)                #Ch6_RX_GAIN
    mySdp.write_spi(0x2016, I_array[index])    #CH6_RX_PHASE_I
    mySdp.write_spi(0x2017, Q_array[index])    #CH6_RX_PHASE_Q
    mySdp.write_spi(0x2028, 0x01)                #Load Work Registers


    #****************** B o a r d B - RX_3  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    bE3Shift = (6 * pshift) % plane
    index = (np.abs(phases-bE3Shift)).argmin()
    #print str(angle_array[index])+'\t'+str(bE3Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 

    mySdp.write_spi(0x2012, 0xff)                #Ch7_RX_GAIN
    mySdp.write_spi(0x2018, I_array[index])    #CH7_RX_PHASE_I
    mySdp.write_spi(0x2019, Q_array[index])    #CH7_RX_PHASE_Q
    mySdp.write_spi(0x2028, 0x01)                #Load Work Registers


    #****************** B o a r d B - RX_4  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    bE4Shift = (7 * pshift) % plane
    index = (np.abs(phases-bE4Shift)).argmin()  
    #print str(angle_array[index])+'\t'+str(bE4Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 

    mySdp.write_spi(0x2013, 0xff)                #Ch8_RX_GAIN
    mySdp.write_spi(0x201A, I_array[index])    #CH8_RX_PHASE_I
    mySdp.write_spi(0x201B, Q_array[index])    #CH8_RX_PHASE_Q
    mySdp.write_spi(0x2028, 0x01)                #Load Work Registers



