# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 


class FirebaseUpload:
    ### RADAR MODULES ###

    def firebaseUploadAcquisition(self, firebaseProject):
        dataJSON = {'Mode': 'Acquisition'} # Insert parameter here in JSON format to also patch phase differnce calculation as an argument from MATLAB
        firebaseProject.patch('/DEV/SignalData', dataJSON)

    def firebaseUploadTracking(self, firebaseProject):
        with open(str(sys.argv[1])+".csv", newline='') as csvfile:
            data1 = list(csv.reader(csvfile)) # Get list from csv file

        dataArray1 = numpy.asarray(data1).ravel().tolist() # Convert list to 2D array, unravel to 1D, and turn back to list

        with open(str(sys.argv[2])+".csv", newline='') as csvfile:
            data2 = list(csv.reader(csvfile)) # Get list from csv file

        dataArray2 = numpy.asarray(data2).ravel().tolist() # Convert list to 2D array, unravel to 1D, and turn back to list

        dataJSON = {'Channel1': dataArray1, 'Channel2': dataArray2, 'Mode': 'Tracking',  'PhaseDifference': 'NA'} # Put data in firebase

        firebaseProject.patch('/DEV/SignalData', dataJSON)


# firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# # Execute function logic here or elsewhere as needed
# firebaseUploadStop(firebaseProject)