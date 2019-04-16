#This script configures registers for the ADAR1000 
#import main
import SDP_driver_new

def ADAR1000A_init(mySdp):
        #Initializing ADAR1000 RX_1 for signal input.
        mySdp.write_spi(0x0000, 0x81)     #Reset the whole board
        mySdp.write_spi(0x0000, 0x18)     #Configure board for SPI communication
        mySdp.write_spi(0x0400, 0x55)     #Adjust LDOs
        mySdp.write_spi(0x0038, 0x60)     #Select SPI for channel settings
        mySdp.write_spi(0x002e, 0x7f)     #Enable LNA
        mySdp.write_spi(0x0034, 0x08)     #Set RX LNA bias to 8
        mySdp.write_spi(0x0035, 0x16)     #Set RX VGA bias to 2
        mySdp.write_spi(0x0031, 0x20)  
        mySdp.write_spi(0x0028, 0x01) 

def ADAR1000B_init(mySdp):
        #Initializing ADAR1000 RX_1 for signal input.
        mySdp.write_spi(0x2000, 0x81)     #Reset the whole board
        mySdp.write_spi(0x2000, 0x18)     #Configure board for SPI communication
        mySdp.write_spi(0x2400, 0x55)     #Adjust LDOs
        mySdp.write_spi(0x2038, 0x60)     #Select SPI for channel settings
        mySdp.write_spi(0x202e, 0x7f)     #Enable LNA
        mySdp.write_spi(0x2034, 0x08)     #Set RX LNA bias to 8
        mySdp.write_spi(0x2035, 0x16)     #Set RX VGA bias to 2
        mySdp.write_spi(0x2031, 0x20)
        mySdp.write_spi(0x2028, 0x01)    #Load Work Registers
