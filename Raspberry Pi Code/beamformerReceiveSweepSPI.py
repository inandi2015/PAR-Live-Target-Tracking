import subprocess

subprocess.call('./spi_initiate')

b_start = -40
#b_end = sys.argv[1]
b_end = 40
b_increment = 10
print "Beamformer Sweeping..."
for angle in (range(b_start, b_end, b_increment)): # at each postion, loop through the beam angles
   instruction = './spi_steer ' + str(angle)
   subprocess.call(instruction)
