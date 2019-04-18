import subprocess

i = 0
while i < 10:
    amp = subprocess.check_output(['python', 'AcquisitionIn.py']).decode('ascii')
    #amp = subprocess.check_output('python AcquisitionIn.py').decode('ascii')
    #subprocess.call('python AcquisitionIn.py', shell=True)
    i = i + 1
    print("Iteration" + str(i))

print(amp.splitlines()[-1])
