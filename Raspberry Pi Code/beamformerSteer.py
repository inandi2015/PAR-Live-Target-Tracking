import time
import sys
import math
import subprocess
import os
import numpy as np

#********************* T a b l e   o f  P h a s e  S e t t i n g s ************
#angle_array = [0, 2.813, 5.625, 8.438, 11.25, 14.063, 16.875, 19.688, 22.5, 25.313, 28.125, 30.938, 33.75, 36.563, 39.375, 42.188, 45, 47.813, 50.625, 53.438, 56.25, 59.063, 61.875, 64.688, 67.5, 70.313, 73.125, 75.938, 78.75, 81.563, 84.375, 87.188, 90, 92.813, 95.625, 98.438, 101.25, 104.063, 106.875, 109.688, 112.5, 115.313, 118.125, 120.938, 123.75, 126.563, 129.375, 132.188, 135, 137.813, 140.625, 143.438, 146.25, 149.063, 151.875, 154.688, 157.5, 160.313, 163.125, 165.938, 168.75, 171.563, 174.375, 177.188, 180, 182.813, 185.625, 188.438, 191.25, 194.063, 196.875, 199.688, 202.5, 205.313, 208.125, 210.938, 213.75, 216.563, 219.375, 222.188, 225, 227.813, 230.625, 233.438, 236.25, 239.063, 241.875, 244.688, 247.5, 250.313, 253.125, 255.938, 258.75, 261.563, 264.375, 267.188, 270, 272.813, 275.625, 278.438, 281.25, 284.063, 286.875, 289.688, 292.5, 295.313, 298.125, 300.938, 303.75, 306.563, 309.375, 312.188, 315, 317.813, 320.625, 323.438, 326.25, 329.063, 331.875, 334.688, 337.5, 340.313, 343.125, 345.938, 348.75, 351.563, 354.375, 357.188]
#I_array = ["3F", "3F", "3F", "3F", "3F", "3E", "3E", "3D", "3D", "3C", "3C", "3B", "3A", "39", "38", "37", "36", "35", "34", "33", "32", "30", "2F", "2E", "2C", "2B", "2A", "28", "27", "25", "24", "22", "21", "01", "03", "04", "06", "07", "08", "0A", "0B", "0D", "0E", "0F", "11", "12", "13", "14", "16", "17", "18", "19", "19", "1A", "1B", "1C", "1C", "1D", "1E", "1E", "1E", "1F", "1F", "1F", "1F", "1F", "1F", "1F", "1F", "1E", "1E", "1D", "1D", "1C", "1C", "1B", "1A", "19", "18", "17", "16", "15", "14", "13", "12", "10", "0F", "0E", "0C", "0B", "0A", "08", "07", "05", "04", "02", "01", "21", "23", "24", "26", "27", "28", "2A", "2B", "2D", "2E", "2F", "31", "32", "33", "34", "36", "37", "38", "39", "39", "3A", "3B", "3C", "3C", "3D", "3E", "3E", "3E", "3F", "3F", "3F"]
#Q_array = ["20", "21", "23", "24", "26", "27", "28", "2A", "2B", "2D", "2E", "2F", "30", "31", "33", "34", "35", "36", "37", "38", "38", "39", "3A", "3A", "3B", "3C", "3C", "3C", "3D", "3D", "3D", "3D", "3D", "3D", "3D", "3D", "3D", "3C", "3C", "3C", "3B", "3A", "3A", "39", "38", "38", "37", "36", "35", "34", "33", "31", "30", "2F", "2E", "2D", "2B", "2A", "28", "27", "26", "24", "23", "21", "20", "01", "03", "04", "06", "07", "08", "0A", "0B", "0D", "0E", "0F", "10", "11", "13", "14", "15", "16", "17", "18", "18", "19", "1A", "1A", "1B", "1C", "1C", "1C", "1D", "1D", "1D", "1D", "1D", "1D", "1D", "1D", "1D", "1C", "1C", "1C", "1B", "1A", "1A", "19", "18", "18", "17", "16", "15", "14", "13", "11", "10", "0F", "0E", "0D", "0B", "0A", "08", "07", "06", "04", "03", "01"]

angle_array=[0.000,2.813,5.625,8.438,11.250,14.063,16.875,19.688,22.500,25.313,28.125,30.938,33.750,36.563,39.375,42.188,45.000,47.813,50.625,53.438,56.250,59.063,61.875,64.688,67.500,70.313,73.125,75.938,78.750,81.563,84.375,87.188,90.000,92.813,95.625,98.438,101.250,104.063,106.875,109.688,112.500,115.313,118.125,120.938,123.750,126.563,129.375,132.188,135.000,137.813,140.625,143.438,146.250,149.063,151.875,154.688,157.500,160.313,163.125,165.938,168.750,171.563,174.375,177.188,180.000,182.813,185.625,188.438,191.250,194.063,196.875,199.688,202.500,205.313,208.125,210.938,213.750,216.563,219.375,222.188,225.000,227.813,230.625,233.438,236.250,239.063,241.875,244.688,247.500,250.313,253.125,255.938,258.750,261.563,264.375,267.188,270.000,272.813,275.625,278.438,281.250,284.063,286.875,289.688,292.500,295.313,298.125,300.938,303.750,306.563,309.375,312.188,315.000,317.813,320.625,323.438,326.250,329.063,331.875,334.688,337.500,340.313,343.125,345.938,348.750,351.563,354.375,357.188]
I_array=["3F","3F","3E","3E","3E","3D","3D","3C","3B","3B","3A","39","38","37","36","35","34","33","32","30","2F","2E","2C","2B","29","28","26","25","23","22","20","01","03","04","06","07","09","0A","0C","0D","0E","10","11","12","13","15","16","17","18","19","1A","1A","1B","1C","1D","1D","1E","1E","1E","1F","1F","1F","1F","1F","1F","1F","1E","1E","1E","1D","1D","1C","1B","1B","1A","19","18","17","16","15","14","13","12","10","0F","0E","0C","0B","09","08","06","05","03","02","00","21","23","24","26","27","29","2A","2C","2D","2E","30","31","32","33","35","36","37","38","39","3A","3A","3B","3C","3D","3D","3E","3E","3E","3F","3F","3F","3F","3F"]
Q_array=["20","22","23","25","26","28","29","2A","2C","2D","2F","30","31","32","34","35","36","37","38","39","3A","3B","3B","3C","3D","3D","3E","3E","3E","3F","3F","3F","3F","3F","3F","3F","3E","3E","3E","3D","3D","3C","3B","3B","3A","39","38","37","36","35","34","32","31","30","2F","2D","2C","2A","29","28","26","25","23","22","20","02","03","05","06","08","09","0A","0C","0D","0F","10","11","12","14","15","16","17","18","19","1A","1B","1B","1C","1D","1D","1E","1E","1E","1F","1F","1F","1F","1F","1F","1F","1E","1E","1E","1D","1D","1C","1B","1B","1A","19","18","17","16","15","14","12","11","10","0F","0D","0C","0A","09","08","06","05","03","02"]

def phaseShift(angle):
    wavelength = 2.498 #cm
    eDist = 1.5 #Distance between each patch antenna elements in centimeters
    plane = 360
    
    #Constant for phase increment. ref: http://www.radartutorial.eu/06.antennas/Phased%20Array%20Antenna.en.html
    pCon = ( plane * eDist ) / wavelength
    #Use formula to calculate phase shift. ref: above
    pShift = pCon * math.sin(math.radians(angle))
    return pShift

# Calculate the I and Q register values and set each channel
def BeamSteering(angle):
    #Calculate phase shift between two elements
    pshift = phaseShift(abs(angle)) 
    #print "angle "+ str(angle) +"\tpshift: " + str(pshift)
    #Copy list of angles into a numerical python array
    phases = np.asarray(angle_array)
    plane = 360
    #writeDelay = 0.01

    #****** C a l c u l a t e  R e g i s t e r  S e t t i n g s ******
    aE1Shift = (0 * pshift) % plane   
    aE2Shift = (1 * pshift) % plane   
    aE3Shift = (2 * pshift) % plane
    aE4Shift = (3 * pshift) % plane
    bE1Shift = (4 * pshift) % plane
    bE2Shift = (5 * pshift) % plane
    bE3Shift = (6 * pshift) % plane
    bE4Shift = (7 * pshift) % plane

    if angle >= 0:
        index1 = (np.abs(phases-aE1Shift)).argmin()
        index2 = (np.abs(phases-aE2Shift)).argmin() 
        index3 = (np.abs(phases-aE3Shift)).argmin() 
        index4 = (np.abs(phases-aE4Shift)).argmin()
        index5 = (np.abs(phases-bE1Shift)).argmin()
        index6 = (np.abs(phases-bE2Shift)).argmin()
        index7 = (np.abs(phases-bE3Shift)).argmin()
        index8 = (np.abs(phases-bE4Shift)).argmin()
    else:
        index8 = (np.abs(phases-aE1Shift)).argmin()
        index7 = (np.abs(phases-aE2Shift)).argmin() 
        index6 = (np.abs(phases-aE3Shift)).argmin() 
        index5 = (np.abs(phases-aE4Shift)).argmin()
        index4 = (np.abs(phases-bE1Shift)).argmin()
        index3 = (np.abs(phases-bE2Shift)).argmin()
        index2 = (np.abs(phases-bE3Shift)).argmin()
        index1 = (np.abs(phases-bE4Shift)).argmin()


    #****************** B o a r d A - RX_1  **************** 
    # 
    #Set the first antenna to 0 degrees    
    
    #//////////////////////////////////////////////////
    #Write to Registers 
    os.system('sudo ./spitest 0010 FF') #Ch1_RX_GAIN
    #time.sleep(writeDelay) # add if needed in between everything
    os.system('sudo ./spitest 0014 ' + I_array[index1]) #CH1_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0015 ' + Q_array[index1]) #CH1_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0028 01') #Load Work Registers
    #print I_array[index1]
    #print Q_array[index1]
    
    #****************** B o a r d A - RX_2  **************** 
    
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(aE2Shift)+'\t'+str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers 
    os.system('sudo ./spitest 0011 FF') #Ch2_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0016 ' + I_array[index2]) #CH2_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0017 ' + Q_array[index2]) #CH2_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0028 01') #Load Work Registers
    #print I_array[index2]
    #print Q_array[index2]

    #****************** B o a r d A - RX_3  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(aE3Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 0012 FF') #Ch3_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0018 ' + I_array[index3]) #CH3_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0019 ' + Q_array[index3]) #CH3_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0028 01') #Load Work Registers
    #print I_array[index3]
    #print Q_array[index3]

    #****************** B o a r d A - RX_4  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(aE4Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 0013 FF') #Ch4_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 001A ' + I_array[index4]) #CH4_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 001B ' + Q_array[index4]) #CH4_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 0028 01') #Load Work Registers
    #print I_array[index4]
    #print Q_array[index4]

    #****************** B o a r d B - RX_1  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(bE1Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 2010 FF') #Ch5_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2014 ' + I_array[index5]) #CH5_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2015 ' + Q_array[index5]) #CH5_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2028 01') #Load Work Registers
    #print I_array[index5]
    #print Q_array[index5]

    #****************** B o a r d B - RX_2  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(bE2Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 2011 FF') #Ch6_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2016 ' + I_array[index6]) #CH6_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2017 ' + Q_array[index6]) #CH6_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2028 01') #Load Work Registers
    #print I_array[index6]
    #print Q_array[index6]

    #****************** B o a r d B - RX_3  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees
    #print str(angle_array[index])+'\t'+str(bE3Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 2012 FF') #Ch7_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2018 ' + I_array[index7]) #CH7_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2019 ' + Q_array[index7]) #CH7_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2028 01') #Load Work Registers
    #print I_array[index7]
    #print Q_array[index7]

    
    #****************** B o a r d B - RX_4  **************** 

    #Apply phase shift to next antenna  
    #Map the angle to a value between 0 and 360 degrees 
    #print str(angle_array[index])+'\t'+str(bE4Shift)+'\t'+ str(I_array[index]) + '\t'+ str(Q_array[index]) 
    #Write to Registers
    os.system('sudo ./spitest 2013 FF') #Ch8_RX_GAIN
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 201A ' + I_array[index8]) #CH8_RX_PHASE_I
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 201B ' + Q_array[index8]) #CH8_RX_PHASE_Q
    #time.sleep(writeDelay)
    os.system('sudo ./spitest 2028 01') #Load Work Registers
    #print I_array[index8]
    #print Q_array[index8]

print "Beamformer Steering..."

BeamSteering(int(sys.argv[1]))
