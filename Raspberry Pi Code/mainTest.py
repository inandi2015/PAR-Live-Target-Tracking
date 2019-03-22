import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase
import time

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

while True: # Outer loop for keeping radar listening continuously
    print('Capstone PAR Alpha System waiting for activation...')
    state = download.firebaseDownloadRadar(firebaseProject)
    if state == 'Start':
        upload.firebaseUploadAcquisition(firebaseProject)
        subprocess.call('python beamformerAcquire.py', shell=True)
        time.sleep(15)
        upload.firebaseUploadTracking(firebaseProject)
        while state != 'Stop': 
            state = download.firebaseDownloadRadar(firebaseProject) # Wait for state to be local
            if state == 'Local': 
                #subprocess.call('python beamformerSweep.py 90', shell=True)
                trackingResult = 'Success'
                if trackingResult == 'Success':
                    subprocess.call('python AnalogIn_Acquisition_2Channel.py', shell=True)
                    if('Stop'):
                        break
                    upload.firebaseUploadTracking(firebaseProject) 
                elif trackingResult == 'Fail':
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
                else: 
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
            else:
                pass
        print("Stopping System")
