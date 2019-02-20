# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

firebase = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
result = firebase.get('/DEV', 'SignalData')
print(result)

dataOut = numpy.asarray(result['data']) # Convert result data from database into an array
dataOut = dataOut.reshape(len(dataOut), 1) # Shape data for putting in one column of csv file

with open(str(sys.argv[1]), "w") as f:
    writer = csv.writer(f, dialect='excel', lineterminator = '\n')
    writer.writerows(dataOut)