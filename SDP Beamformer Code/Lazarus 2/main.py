# Author: Frank Manu
# Reference: Benjamin Sam
# Date: 04/12/2018
# Purpose: This is the main file for the system
import config 
import pilot
from SDP_driver_new import *
from lazarus import clearScrn 
from lazarus import kill
from jemma import *

def starter():
    
    print 'Attempting to connect....'
    
    hw_id = ['6065711100000001']
    mySdp = connect_sdp(hw_id, sclkFrequency=2e6)
    
    # Show whether the connection was successful
    if mySdp.connected: 
        print '\n\t\t\t  Connection Successful!'
        print '\t\t\t**************************\n'
        
        #Configure Board A (primary board)
        config.ADAR1000A_init(mySdp)
        #Configure Board B (secondary board)
        config.ADAR1000B_init(mySdp)
        
        #Point Beam to an angle
        usrOptions() 

        Command = getCommand()
        while (Command == '1' or Command == '2' or Command == '3' or Command == '4' or Command == '5' or Command == '6' or Command == '7'
                or Command == "exit" or Command == "EXIT" or Command == "Exit"  or Command == 'o'  or Command == 'O'  or Command == '0'
                 or Command == '8') :
            if Command =='1':
                angle = input("Enter angle: ")

                while(angle > 180 or angle < 0):
                    print('Out of Scanning Range')
                    angle = input("Enter angle: ")

                pilot.setCourse(mySdp, angle)
                Command = getCommand()

            elif Command =='2':
                angle = input("Enter angle: ")
               
                while(angle > 180 or angle < 0):
                    print('Out of Scanning Range')
                    angle = input("Enter angle: ")
                pilot.setCourse1(mySdp, angle)
                Command = getCommand() 

            #Perform beamsteering to find target 
            elif Command == '3':
                print("Scanning...")
                pilot.sweep(mySdp)
                Command = getCommand()
            
            elif Command == '4':
                print("Quick Scan...")
                pilot.sweep1(mySdp)
                Command = getCommand()

            elif Command == '5':
                angle = input("Enter angle: ")
                while(angle > 180 or angle < 0):
                    print('Out of Scanning Range')
                    angle = input("Enter angle: ")
                pilot.steer(mySdp, angle)
                print("Steering Complete. Pointing towards: "+ str(angle) + " degrees")
                Command = getCommand()
            
            elif Command == '6':
                print("\n\t\tACTIVATING CONTINOUS SCAN MODE") 
                print("\t\tTo Quit Press \'ENTER\' At Any Time ")
                pilot.conScan(mySdp)
                Command = getCommand()
            
            elif Command == '7':
                getHelp()
                Command = getCommand()

            elif (Command == "exit" or Command == "Exit" or Command == "EXIT" or Command == '8'):
                print ("Exiting Program")
                break
            
            elif (Command == "O" or Command == 'o' or Command == '0'):
                usrOptions()
                Command = getCommand()

            else:
                print("Command Not Recognized: Try Again") 
                Command = getCommand()

    else:
        print '\n\tNo connection made...'



if __name__ == '__main__':
    kill()
    clearScrn()
    header()
    starter()