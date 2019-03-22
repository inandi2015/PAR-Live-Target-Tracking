import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase 

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
subprocess.call('python initializeAD.py', shell=True)

while True: # Outer loop for keeping radar listening continuously
    print('Capstone PAR Alpha System waiting for activation...')
    state = download.firebaseDownloadRadar(firebaseProject)
    if state == 'Start':
        upload.firebaseUploadAcquisition(firebaseProject)
        subprocess.call('python beamformerAcquire.py', shell=True)
        while state != 'Stop': 
            state = download.firebaseDownloadRadar(firebaseProject) # Wait for state to be local
            if state == 'Local': 
                subprocess.call('python beamformerSweep.py 90', shell=True)
                trackingResult = 'Success'
                if trackingResult == 'Success':
                    subprocess.call('python getSignal.py', shell=True)
                    upload.firebaseUploadTracking(firebaseProject) 
                elif trackingResult == 'Fail':
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
                else: 
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
            else:
                pass
