import subprocess

i = 0
while i < 1:
    #amp = subprocess.check_output(['python', 'AcquisitionIn.py']).decode('ascii')
    #amp = subprocess.check_output('python AcquisitionIn.py').decode('ascii')
    subprocess.call('python AcquisitionIn.py', shell=True)
    i = i + 1
    print("Iteration" + str(i))

with open('amplitude.txt', 'r') as file:
        data = file.read()

print(data)

#print(amp.splitlines()[-1])
