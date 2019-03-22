# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

class FirebaseDownload:
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
            return 'Start'
        elif result['Mode'] == 'Stop':  
            #print("Stopping system...")
            # Kill everything
            return 'Stop'
        elif result['Mode'] == 'Local':
            print("Steering beamformer...")
            # Return phase difference result['PhaseDifference'] to steer beam
            return 'Local'
        
