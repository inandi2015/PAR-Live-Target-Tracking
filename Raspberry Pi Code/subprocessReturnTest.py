import subprocess
test = subprocess.check_output('python beamformerAcquire.py').decode('ascii')
print(test)