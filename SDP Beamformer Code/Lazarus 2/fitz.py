import math
import numpy as np
import matplotlib.pyplot as plt
#****** S H I F T () **********************************************************
#
#   This function returns the calculated phase shift between two successive elements
#   depending on the steering angle
#
#*********************************************************************************
def phaseShift(angle):
    wavelength = 2.778 #cm
    eDist = 1.5 #Distance between each patch antenna elements in centimeters
    plane = 360
    
    #Constant for phase increment. ref: http://www.radartutorial.eu/06.antennas/Phased%20Array%20Antenna.en.html
    pCon = ( plane * eDist ) / wavelength
    #Use formula to calculate phase shift. ref: above
    pShift = pCon * math.sin(math.radians(angle))
    return pShift

def sweepGrab():
    x_1 = np.loadtxt('ch1Samples.txt', float,'#', ',')
    x1_max = np.amax(x_1)
    x_2 = np.loadtxt('ch2Samples.txt', float,'#', ',')
    x2_max = np.amax(x_2)
    total_max = x1_max + x2_max
    return total_max

def sweepGrab1():
    x_1 = np.loadtxt('ch1Samples.txt', float,'#', ',')
    x_2 = np.loadtxt('ch2Samples.txt', float,'#', ',')
    total_max = x_1+ x_2
    return total_max

def plot(angle, dist = 3):
    theta = math.radians(angle)
    r = dist
    ax = plt.subplot(111,polar=True)
    ax.scatter(0,15, marker = '_')
    ax.scatter(theta,r, c = 'r')
    ax.set_facecolor((0.08, 0.7, 0.023))
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    plt.show()