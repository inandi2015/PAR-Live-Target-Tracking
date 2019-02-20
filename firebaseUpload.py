# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

firebase = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

with open(str(sys.argv[1]), newline='') as csvfile:
    data = list(csv.reader(csvfile)) # Get list from csv file

dataArray = numpy.asarray(data).ravel().tolist() # Convert list to 2D array, unravel to 1D, and turn back to list
dataJSON = {'data': dataArray} # Put data in firebase

firebase.patch('/DEV/SignalData', dataJSON)