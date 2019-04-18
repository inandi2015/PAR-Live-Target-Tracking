import subprocess

i = 0
while i < 10:
    amp = subprocess.check_output('python Sweep.py').decode('ascii')
    i = i + 1
    print("Iteration" + str(i))

print(amp.splitlines()[-1])