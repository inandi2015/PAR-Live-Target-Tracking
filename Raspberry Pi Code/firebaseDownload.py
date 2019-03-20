# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

class firebaseDownload:
    ### RADAR MODULES ###

    def firebaseDownloadRadar(self, firebaseProject):
        while True:
            result = firebaseProject.get('/DEV', 'SignalData')
            if result['Mode'] == 'Start' or result['Mode'] == 'Stop' or result['Mode'] == 'Local':
                break

        print(result['Mode'])
        print(result['PhaseDifference'])
        
        if result['Mode'] == 'Start':
            print("Starting system...")
            # Call driver stuff
        elif result['Mode'] == 'Stop':  
            print("Stopping system...")
            # Kill everything
        elif result['Mode'] == 'Local':
            print("Steering beamformer...")
            # Return phase difference result['PhaseDifference'] to steer beam
        

# firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# firebaseDownloadRadar(firebaseProject)