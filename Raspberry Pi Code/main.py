import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase
import time
import sys

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

# Sample program run: python3 main.py 0.1 7 10
beamformerThreshold = float(sys.argv[1]) # Amplitude setting for threshold
beamformerPositions = int(sys.argv[2]) # Number of beamformerpositions, for 7, it's (-60, -40, -20, 0, 20, 40, 60)
offsetAngle = int(sys.argv[3]) # Set how far to steer to left or right for tracking target
degreesOfFreedom = 120 # Degrees of freedom for the beamformer steering
angleCorrection = 60 # Set 120 degrees of freedom from 0 to 120 to be -60 to 60 with an offset of 60
timeoutVal = 5 # Timeout for Waveforms in case it gets hung up

waitStart = True
while True: # Outer loop for keeping radar listening continuously
    if waitStart == True:
        print('Capstone PAR Alpha System waiting for activation...')
        waitStart = False
    state, phase = download.firebaseDownloadRadar(firebaseProject)
    if state == 'Start':
        subprocess.call('python beamformerInitialize.py', shell=True) # Initialize beamformer

        while state != 'Stop': 
            # Acquisition Mode
            upload.firebaseUploadAcquisition(firebaseProject)
            state, phase = download.firebaseDownloadRadar(firebaseProject) # Check status of firebase
            if state == 'Stop':
                break
            amplitudeValues = []
            # Check every angle with beamformer
            for i in range(beamformerPositions): # for i=0 to i=(beamformerPositions-1)
                positionNumber = int(i)
                angleDivision = int(degreesOfFreedom/int(beamformerPositions-1))
                position = positionNumber * angleDivision - angleCorrection
                subprocess.call('python beamformerSteer.py ' + str(position), shell=True)
                print("Acquiring amplitude...")
                amplitude = -1
                while amplitude == -1:
                    try:
                        amplitude = subprocess.check_output(['python', 'AcquisitionIn.py'], timeout=timeoutVal).decode('ascii')
                    except subprocess.TimeoutExpired:
                        print("Timeout happened. Retrying...\n")
                print("Done acquiring!")

                if str(amplitude.splitlines()[-1]) != "failed to open device":
                    print("Amplitude found: " + amplitude.splitlines()[-1])
                    amplitudeValues.append(float(amplitude.splitlines()[-1]))
                else:
                    i = i - 1 # Retest the previous position
            
            if max(amplitudeValues) > beamformerThreshold:
                maxAmplitudeIndex = amplitudeValues.index(max(amplitudeValues))
                print("Target found. Repositioning for tracking")
                positionNumber = int(maxAmplitudeIndex)
                angleDivision = int(degreesOfFreedom/int(beamformerPositions-1))
                position = positionNumber * angleDivision - angleCorrection
                subprocess.call('python beamformerSteer.py ' + str(position), shell=True)

                print("Measuring amplitude...")
                amplitude = -1
                while amplitude == -1:
                    try:
                        amplitude = subprocess.check_output(['python', 'AcquisitionIn.py'], timeout=timeoutVal).decode('ascii')
                    except subprocess.TimeoutExpired:
                        print("Timeout happened. Retrying...\n")

                upload.firebaseUploadTracking(firebaseProject, int(position)) 
                currentAngle = int(maxAmplitudeIndex) * int(180/int(beamformerPositions-1))
                while state != 'Stop': 
                    # Tracking Mode
                    state, phase = download.firebaseDownloadRadar(firebaseProject) # Wait for state to be local
                    if state == 'Stop':
                        break
                    if state == 'Local':
                        if float(phase) > 0:
                            print("Steer right!")
                            currentAngle = currentAngle + offsetAngle
                            subprocess.call('python beamformerSteer.py ' + str(currentAngle), shell=True)
                        elif float(phase) < 0:
                            print("Steer left!")
                            currentAngle = currentAngle - offsetAngle
                            subprocess.call('python beamformerSteer.py ' + str(currentAngle), shell=True)

                        print("Measuring amplitude...")
                        amplitude = -1
                        while amplitude == -1:
                            try:
                                amplitude = subprocess.check_output(['python', 'AcquisitionIn.py'], timeout=timeoutVal).decode('ascii')
                            except subprocess.TimeoutExpired:
                                print("Timeout happened. Retrying...\n")

                        if float(amplitude.splitlines()[-1]) > beamformerThreshold:
                            # state, phase = download.firebaseDownloadRadar(firebaseProject) 
                            # if state == 'Stop':
                            #     break
                            upload.firebaseUploadTracking(firebaseProject, int(position))  
                        else:
                            print("Lost target. Acquiring target again...")
                            break # Go back to acquisition
                    else:
                        pass
        waitStart = True
        print("Stopping System...")
