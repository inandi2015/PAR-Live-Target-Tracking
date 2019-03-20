# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

class FirebaseUpload:
    ### LOCAL MODULES ###

    def firebaseUploadStart(self, firebaseProject):
        dataJSON = {'Mode': 'Start', 'PhaseDifference': 'NA'}
        firebaseProject.patch('/DEV/SignalData', dataJSON)

    def firebaseUploadStop(self, firebaseProject):
        dataJSON = {'Mode': 'Stop', 'PhaseDifference': 'NA'}
        firebaseProject.patch('/DEV/SignalData', dataJSON)

    def firebaseUploadLocal(self, firebaseProject, phaseDifference):
        dataJSON = {'Mode': 'Local', 'PhaseDifference': phaseDifference} # Insert parameter here in JSON format to also patch phase differnce calculation as an argument from MATLAB
        firebaseProject.patch('/DEV/SignalData', dataJSON)


# firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# # Execute function logic here or elsewhere as needed
# firebaseUploadStop(firebaseProject)