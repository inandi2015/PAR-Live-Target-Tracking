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
            if result['Mode'] == 'Start' or result['Mode'] == 'Stop' or result['Mode'] == 'Local' or result['Mode'] == 'Acquisition':
                break

        #print(result['Mode'])
        #print(result['PhaseDifference'])
        
        if result['Mode'] == 'Start':
            print("Starting system...")
            # Call driver stuff
            return 'Start', 'NA'
        elif result['Mode'] == 'Stop':  
            #print("Stopping system...")
            # Kill everything
            return 'Stop', 'NA'
        elif result['Mode'] == 'Local':
            #print("Steering beamformer...")
            phaseDifference = result['PhaseDifference']
            # Return phase difference result['PhaseDifference'] to steer beam
            return 'Local', phaseDifference
        elif result['Mode'] == 'Acquisition':
            return 'NA', 'NA' 
