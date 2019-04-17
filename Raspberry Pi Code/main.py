import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase
import time

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

beamformerThreshold = 10.0 # Amplitude setting for threshold
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
            beamformerPositions = 5
            for i in range(beamformerPositions): # for i=0 to i=(beamformerPositions-1)
                subprocess.call('python beamformerSteer.py ' + str(i) + ' ' + str((beamformerPositions-1)), shell=True)
                amplitude = subprocess.check_output('python AcquisitionIn.py').decode('ascii')
                if (amplitude.splitlines()[-1]) != "failed to open device":
                    amplitudeValues.append(float(amplitude.splitlines()[-1]))
                else:
                    i = i - 1 # Retest the previous position
            
            if max(amplitudeValues) > beamformerThreshold:
                maxAmplitudeIndex = amplitudeValues.index(max(amplitudeValues))
                print("Target found. Repositioning for tracking")
                subprocess.call('python beamformerSteer.py ' + str(maxAmplitudeIndex) + ' ' + str((beamformerPositions-1)), shell=True)
                amplitude = subprocess.check_output('python AcquisitionIn.py').decode('ascii')

                upload.firebaseUploadTracking(firebaseProject)
                currentPosition = maxAmplitudeIndex
                while state != 'Stop': 
                    # Tracking Mode
                    state, phase = download.firebaseDownloadRadar(firebaseProject) # Wait for state to be local
                    if state == 'Stop':
                        break
                    if state == 'Local':
                        if float(phase) > 0:
                            currentPosition = currentPosition + 1
                            subprocess.call('python beamformerSteer.py ' + str(currentPosition) + ' ' + str((beamformerPositions-1)), shell=True)
                        elif float(phase) < 0:
                            currentPosition = currentPosition - 1
                            subprocess.call('python beamformerSteer.py ' + str(currentPosition) + ' ' + str((beamformerPositions-1)), shell=True)
                        amplitude = subprocess.check_output('python AcquisitionIn.py').decode('ascii')         
                        if float(amplitude.splitlines()[-1]) > beamformerThreshold:
                            # state, phase = download.firebaseDownloadRadar(firebaseProject)
                            # if state == 'Stop':
                            #     break
                            upload.firebaseUploadTracking(firebaseProject) 
                        else:
                            break # Go back to acquisition
                    else:
                        pass
        waitStart = True
        print("Stopping System...")
