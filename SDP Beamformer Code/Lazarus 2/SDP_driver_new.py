#Annotated By Frank M.

import clr
import sdpApi1
from time import sleep
import sys
    

def connect_sdp(hwid_list, *_args, **_kwargs):
    # Method to connect to an SDP board from a list of IDs you want to maintain
    # If there's only one item in the list, connect to it
    if len(hwid_list) == 1:
        return Sdp(hwid_list[0], *_args, **_kwargs)

    # If there are multiple IDs to choose from
    else:
        # Check for boards matching the IDs given
        sdpApi1.SdpManager.connectMultiDialog(hwid_list, 0, None)

        # Get the response and list of available boards. Initialize the index to 0
        board_idx = 0
        text, out_lst = sdpApi1.SdpManager.connectUsrDialogList(False, False, board_idx, None, None)[-2:]

        # If no boards were found, print that and move on
        if 'no matching systems found' in text.lower():
            print '\n\tNo matching systems found...'

        # If one or more boards were found
        elif len(out_lst) >= 1:
            # Start an infinite loop
            while True:
                # If more than 1 board was found
                if len(out_lst) > 1:
                    try:
                        # Print the available boards
                        print '\nAvailable Boards:'
                        for n, name in enumerate(out_lst):
                            print '\t%s -> %s: "%s"' % (n, name.split(':\n')[0], name.split(':\n')[1])

                        # Ask which board you'd like to connect to
                        resp = input('\nSelect a board to connect to:\t')

                        # If the user response was invalid, throw an error
                        if (resp < 0) or (resp > len(out_lst) - 1):
                            raise ValueError

                        # Set the index to the requested board and break out of the loop
                        sdpApi1.SdpManager.connectUsrDialogList(False, False, resp, None, None)
                        break

                    # If an error is thrown, show the user
                    except (NameError, ValueError):
                        print '\n\tInvalid selection! Please try again.'

                # If only 1 board was found, the index is already correct, so break out of the loop
                else:
                    break

            # Connect to the currently indexed board
            sdp = sdpApi1.SdpManager.connectUsrDialog(None)[1]

            # Determine which ID you connected to
            hw_id = sdp.SystemDescription.DaughterBoards[0].UniqueId

            # Close the connection
            sdp.resetAndDisconnect()

            # Return an Sdp class handle using the ID we wanted. This gives you access to the driver's functions
            return Sdp(hw_id, *_args, **_kwargs)
        else:
            # Print the response
            print '\n%s' % text

        # Return a dummy SDP handle
        return Sdp('dummy')


def set_to_multiple(value, multiple=8):
    # Change a number to a multiple of another number, if it isn't already
    multiplier = int(value / multiple)
    remainder = value % multiple

    # If we're more than halfway between two multiples, increase the multiplier
    if remainder > 4:
        multiplier += 1

    # Return the value
    return multiple * multiplier


class Sdp:
    def __init__(self, hw_id, connector=0, slaveSelect=0, wordSize=24, cpol=False, cpha=False, lsbFirst=False,
                 sclkFrequency=10e6, frameFrequency=100e3, bus=0, slaveAddress=50, sclFrequency=400, dutyCycle=50):
        # Initialize the SDP connection to the daughter board

        # SPI inputs
        self.slaveSelect = slaveSelect
        self.wordSize = wordSize
        self.cpol = cpol
        self.cpha = cpha
        self.lsbFirst = lsbFirst
        self.sclkFrequency = sclkFrequency
        self.frameFrequency = frameFrequency

        # I2C inputs
        self.bus = bus
        self.slaveAddress = slaveAddress
        self.sclFrequency = sclFrequency
        self.dutyCycle = dutyCycle

        # Initialize the Daughter board info
        self.description = 'Dummy Description'
        self.name = 'Dummy Name'

        # Initialize the connected flag
        self.connected = False

        # Connect to the SDP board using the HWID #
        if 'dummy' not in hw_id.lower():
            self.sdp = sdpApi1.SdpManager.connect(hw_id, '', False, None)[1]

            # Define the SPI handle
            self.spi = self.sdp.newSpi(connector, slaveSelect, wordSize, cpol, cpha, lsbFirst, sclkFrequency,
                                       frameFrequency, None)[1]

            # Define the GPIO handle
            self.gpio = self.sdp.newGpio(connector, None)[1]

            # Define the I2C handle
            self.i2c = self.sdp.newI2c(connector, bus, slaveAddress, sclFrequency, dutyCycle, None)[1]

            # Get the Daughter board info
            self.description = self.sdp.SystemDescription.DaughterBoards[0].Description
            self.name = self.sdp.SystemDescription.DaughterBoards[0].Name
            self.hwid = self.sdp.SystemDescription.DaughterBoards[0].UniqueId

            # Get the connected flag
            self.connected = self.sdp.connected

    def configure_gpio(self, which='output', bit_mask=0xFF, initial=None):
        # Configure the GPIO pins to be inputs or outputs

        # Set the bitmask
        if 'out' in which.lower():
            # Set the required outputs
            self.gpio.configOutput(bit_mask)
        elif 'in' in which.lower():
            # Set the required outputs
            self.gpio.configInput(bit_mask)

        # Set up the bit initial states, if requested
        if initial:
            self.gpio_write(initial)
        return

    def configure_gpio_spi(self, csb=0, sclk=1, mosi=2, miso=3, use_miso=False):
        # Check to be sure that the lines are all different
        if csb in (sclk, mosi, miso):
            raise ValueError
        if sclk in (csb, mosi, miso):
            raise ValueError
        if mosi in (csb, sclk, miso):
            raise ValueError
        if miso in (csb, sclk, mosi):
            raise ValueError

        # Configure the miso GPIO line to be an input
        if use_miso:
            self.configure_gpio('input', (1 << miso))

        # Configure the csb, sclk, and mosi GPIO lines to be outputs and initialize the CSB line to 1
        self.configure_gpio(bit_mask=((1 << csb) | (1 << sclk) | (1 << mosi)), initial=(1 << csb))
        return

    def flash_led(self):
        # Flash the LED on the SDP board
        self.sdp.flashLed1()
        return

    def gpio_write(self, bit_data):
        # Write to the GPIO pins
        ret = self.gpio.dataWrite(bit_data)
        return ret

    def gpio_read(self):
        # Read the GPIO pins statuses
        ret, byte = self.gpio.dataRead(0xFF)
        return ret, byte

    def gpio_spi_read(self, address, csb_pin=0, sclk_pin=1, mosi_pin=2, miso_pin=3, addr_bits=16, data_bits=8,
                      three_wire=False):
        # Read a register with SPI using the GPIO lines

        # Set the GPIO lines to the correct state
        self.configure_gpio(bit_mask=((1 << csb_pin) | (1 << sclk_pin) | (1 << mosi_pin)))
        self.configure_gpio('input', bit_mask=(1 << miso_pin))

        # Change the address bits to a multiple of 8 if it isn't already
        if addr_bits % 8:
            addr_bits = set_to_multiple(addr_bits)

        # Determine how long to make each signal. The clock needs twice as many operations as the data
        write_bits = addr_bits + data_bits
        clk_edges = 2 * write_bits

        # Create the csb list with 1s on the outside and 0s in the middle.
        # Making it longer than the sclk and data streams so that we're sure to not cut off the other lines
        csb_list = [1] + ([0] * (clk_edges + 2)) + [1]

        # Initialize the sclk list and build the rest
        sclk_list = [0, 0, 0]

        # Start off with a 0 so that the first clock bit is high (it gets inverted)
        curr_sclk = 0

        # We can shorten the loop since the first sclk bit will be a rising edge
        # and we've already accounted for the first 0 in the instantiation above
        for i in xrange(clk_edges - 1):

            # Toggle sclk
            curr_sclk = abs(1 - curr_sclk)

            # Append the point to the list
            sclk_list.append(curr_sclk)

        # Pad the end of the list with 0s
        sclk_list += [0, 0]

        # MOSI needs to follow the address and data info, but at half the frequency of the clock
        # Build a binary string representing the data to send. Need to add the read bit to the address as well
        send_str = format((1 << (addr_bits + data_bits - 1)) | (address << data_bits), '0%sb' % write_bits)

        # Initialize the mosi list
        mosi_list = [0, 0]

        # Go through the bits and add the current value to the mosi list twice. This halves the frequency
        for bit in send_str:
            mosi_list += [int(bit), int(bit)]

        # Pad the rest of the mosi list with 0s
        mosi_list += [0, 0]

        # Initialize a readback string
        readback = ''

        # Clock counter variable to know when we've begun the readback stage
        clk_count = 0

        # Go through the lists and write the GPIO accordingly
        for bit in xrange(len(csb_list)):
            # Grab the current bits and shift them to the correct place in the GPIO bit mask
            csb_val = (csb_list[bit] << csb_pin)
            sclk_val = (sclk_list[bit] << sclk_pin)
            mosi_val = (mosi_list[bit] << mosi_pin)

            # Put the signals together
            curr_sig = (csb_val | sclk_val | mosi_val)

            # Write the GPIO lines
            self.gpio_write(curr_sig)

            # Wait a millisecond at blocks of 8 clock edges
            if clk_count and not clk_count % 8 and clk_count != (write_bits - 1):
                sleep(0.001)

            # If we're at the read section
            if clk_count >= addr_bits:
                if three_wire:
                    # Change the mosi line to an input if we're reading and in 3 wire mode
                    self.configure_gpio('input', bit_mask=(1 << mosi_pin))

                # If sclk was high
                if sclk_val:
                    status, value = self.gpio_read()
                    if three_wire:
                        value = ((value >> mosi_pin) & 1)
                    else:
                        value = ((value >> miso_pin) & 1)

                    # Add the bit to the readback string
                    readback += str(value)

            # Increment the clock counter
            if sclk_val:
                clk_count += 1

        # Change the mosi line back to an output, if necessary
        if three_wire:
            self.configure_gpio(bit_mask=(1 << mosi_pin))

        # Convert the readback to a number and return it
        return int(readback, 2)

    def gpio_spi_read_write(self, address, data, csb_pin=0, sclk_pin=1, mosi_pin=2, miso_pin=3, addr_bits=16,
                            data_bits=8, three_wire=False):
        # Write a SPI command with the GPIO lines and then read the result
        self.gpio_spi_write(address, data, csb_pin, sclk_pin, mosi_pin, addr_bits, data_bits)
        readback = self.gpio_spi_read(address, csb_pin, sclk_pin, mosi_pin, miso_pin, addr_bits, data_bits, three_wire)
        return readback

    def gpio_spi_write(self, address, data, csb_pin=0, sclk_pin=1, mosi_pin=2, addr_bits=16, data_bits=8):
        # Write a SPI command with the GPIO lines

        # Set the GPIO lines to the correct state
        self.configure_gpio(bit_mask=((1 << csb_pin) | (1 << sclk_pin) | (1 << mosi_pin)))

        # Change the address bits to a multiple of 8 if it isn't already
        if addr_bits % 8:
            addr_bits = set_to_multiple(addr_bits)

        # Determine how long to make each signal. The clock needs twice as many operations as the data
        write_bits = addr_bits + data_bits
        clk_edges = 2 * write_bits

        # Create the csb list with 1s on the outside and 0s in the middle.
        # Making it longer than the sclk and data streams so that we're sure to not cut off the other lines
        csb_list = [1] + ([0] * (clk_edges + 2)) + [1]

        # Initialize the sclk list and build the rest
        sclk_list = [0, 0, 0]

        # Start off with a 0 so that the first clock bit is high
        curr_sclk = 0

        # We can shorten the loop since the first sclk bit will be a rising edge
        for i in xrange(clk_edges - 1):

            # Toggle sclk
            curr_sclk = abs(1 - curr_sclk)

            # Append the point to the list
            sclk_list.append(curr_sclk)

        # Pad the end of the list with 0s
        sclk_list += [0, 0]

        # MOSI needs to follow the address and data info, but at half the frequency of the clock
        # Build a binary string representing the data to send
        send_str = format(((address << data_bits) | data), '0%sb' % write_bits)

        # Initialize the mosi list
        mosi_list = [0, 0]

        # Go through the bits and add the current value to the mosi list twice. This halves the frequency
        for bit in send_str:
            mosi_list += [int(bit), int(bit)]

        # Pad the rest of the mosi list with 0s
        mosi_list += [0, 0]

        # Initialize a clock edge counter
        clk_count = 0

        # Go through the lists and write the GPIO accordingly
        for bit in xrange(len(csb_list)):
            # Grab the current bits and shift them to the correct place in the GPIO bit mask
            csb_val = (csb_list[bit] << csb_pin)
            sclk_val = (sclk_list[bit] << sclk_pin)
            mosi_val = (mosi_list[bit] << mosi_pin)

            # Put the entire mask together
            bit_mask = (csb_val | sclk_val | mosi_val)

            # Write the GPIO lines
            self.gpio_write(bit_mask)

            # Wait a millisecond at blocks of 8 clock edges
            if clk_count and not clk_count % 8 and clk_count != (write_bits - 1):
                sleep(0.001)

            # Increment the counter at rising clock edges
            if sclk_val:
                clk_count += 1
        return

    def gpio_toggle(self, bit_mask):
        # Toggle the masked bits
        ret = self.gpio.bitToggle(bit_mask)
        return ret

    def read_spi(self, address, addr_bits=16, data_bits=8):
        # Read from an address with the SPI.

        # Change the address bits to a multiple of 8 if it isn't already
        if addr_bits % 8:
            addr_bits = set_to_multiple(addr_bits)

        # In data needs to be a list.
        # The read bit is shifted 1 bit less than the total of the address and read bits
        in_data = [(1 << (addr_bits + data_bits - 1)) | (address << data_bits)]

        # Set the word size
        self.spi.wordSize = addr_bits + data_bits

        # Run the transaction
        if self.spi.wordSize == 8:
            ret, value = self.spi.writeReadU8(in_data, 1, None)
            mask = 0xF
        elif self.spi.wordSize == 16:
            ret, value = self.spi.writeReadU16(in_data, 1, None)
            mask = 0xFF
        elif self.spi.wordSize == 24:
            ret, value = self.spi.writeReadU24(in_data, 1, None)
            mask = 0xFFF
        elif self.spi.wordSize == 32:
            ret, value = self.spi.writeReadU32(in_data, 1, None)
            mask = 0xFFFF
        else:
            raise NotImplementedError

        # Readback comes out in a list. Mask out any irrelevant bits
        value = value[0] & mask

        # Return the status bit and value
        return ret, value

    def read_write_spi(self, address, input_data, addr_bits=16, data_bits=8):
        # Write and read an address with the SPI.

        # Write to the SPI port
        write_status = self.write_spi(address, input_data, addr_bits=addr_bits, data_bits=data_bits)

        # Read back from the SPI port
        read_status, read_value = self.read_spi(address, addr_bits=addr_bits, data_bits=data_bits)

        # Return the status bits and readback value
        return write_status, read_status, read_value

    def write_spi(self, address, input_data, addr_bits=16, data_bits=8):
        # Write to an address with the SPI.

        # Change the address bits to a multiple of 8 if it isn't already
        if addr_bits % 8:
            addr_bits = set_to_multiple(addr_bits)

        # Input data needs to be in a list
        in_data = [address << data_bits | input_data]

        # Set the word size
        self.spi.wordSize = addr_bits + data_bits

        # Run the transaction and get the status bit
        if self.spi.wordSize == 8:
            ret = self.spi.writeU8(in_data)
        elif self.spi.wordSize == 16:
            ret = self.spi.writeU16(in_data)
        elif self.spi.wordSize == 24:
            ret = self.spi.writeU24(in_data)
        elif self.spi.wordSize == 32:
            ret = self.spi.writeU32(in_data)
        else:
            raise NotImplementedError

        # Return the status bit
        return ret