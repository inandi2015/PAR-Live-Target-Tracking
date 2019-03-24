import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase
import time

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

waitStart = True
adResult = 'Fail'
print("Starting program")
while True: # Outer loop for keeping radar listening continuously
    if waitStart == True:
        print('Capstone PAR Alpha System waiting for activation...')
        waitStart = False
    state = download.firebaseDownloadRadar(firebaseProject)
    if state == 'Start':
        upload.firebaseUploadAcquisition(firebaseProject)
        subprocess.call('python beamformerAcquire.py', shell=True)
        time.sleep(5)
        upload.firebaseUploadTracking(firebaseProject)
        while state != 'Stop': 
            state = download.firebaseDownloadRadar(firebaseProject) # Wait for state to be local
            if state == 'Local': 
                #subprocess.call('python beamformerSweep.py 90', shell=True)
                trackingResult = 'Success'
                if trackingResult == 'Success':
                    while adResult == 'Fail'
                        adResult = subprocess.subprocess.check_output('python AnalogIn_Acquisition_2Channel.py', shell=True).decode('ascii')
                        if adResult == 'Fail':
                            print("Analog Discovery failed. Retrying...")
                        else 
                            print("Analog Discovery data acquired!")
                    adResult = 'Fail'   
                    state = download.firebaseDownloadRadar(firebaseProject)
                    if state == 'Stop':
                        break
                    print("Uploading tracking data...")
                    upload.firebaseUploadTracking(firebaseProject) 
                elif trackingResult == 'Fail':
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
                else: 
                    upload.firebaseUploadAcquisition(firebaseProject)
                    subprocess.call('python beamformerAcquire.py', shell=True)
            else:
                pass
        waitStart = True
        print("Stopping System")
