# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

### POST ANY MODE BY ITSELF TO FIREBASE ###

def firebaseUploadStart(firebaseProject):
    dataJSON = {'Mode': 'Start'}
    firebaseProject.patch('/DEV/SignalData', dataJSON)

def firebaseUploadStop(firebaseProject):
    dataJSON = {'Mode': 'Stop'}
    firebaseProject.patch('/DEV/SignalData', dataJSON)

def firebaseUploadLocal(firebaseProject):
    dataJSON = {'Mode': 'Local'} # Insert parameter here in JSON format to also patch phase differnce calculation as an argument from MATLAB
    firebaseProject.patch('/DEV/SignalData', dataJSON)
    
def firebaseUploadAcquisition(firebaseProject):
    dataJSON = {'Mode': 'Acquisition'} # Insert parameter here in JSON format to also patch phase differnce calculation as an argument from MATLAB
    firebaseProject.patch('/DEV/SignalData', dataJSON)

def firebaseUploadTracking(firebaseProject):
    dataJSON = {'Mode': 'Tracking'} # Insert parameter here in JSON format to also patch phase differnce calculation as an argument from MATLAB
    firebaseProject.patch('/DEV/SignalData', dataJSON)

firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

# CALL WHATEVER FUNCTION FOR WHATEVER MODE YOU WANT TO UPLOAD HERE
if sys.argv[1] == 'Start':
    firebaseUploadStart(firebaseProject)
elif sys.argv[1] == 'Stop':
    firebaseUploadStop(firebaseProject)
elif sys.argv[1] == 'Local':
    firebaseUploadLocal(firebaseProject)
elif sys.argv[1] == 'Acquisition':
    firebaseUploadAcquisition(firebaseProject)
elif sys.argv[1] == 'Tracking':
    firebaseUploadTracking(firebaseProject)
else:
    firebaseUploadLocal(firebaseProject) # Whatever default you want