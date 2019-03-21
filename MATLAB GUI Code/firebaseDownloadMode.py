# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

### POST ANY MODE BY ITSELF TO FIREBASE ###

def firebaseDownloadLocal(firebaseProject):
    result = firebaseProject.get('/DEV', 'SignalData')

    print(result['Mode'])
    
    # Write to a CSV file here the aquisition mode so MATLAB can check it
    with open(str("OutputStatus.csv", "w") as f:
        writer = csv.writer(f, dialect='excel', lineterminator = '\n')
        writer.writerow([result['Mode']])

firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
firebaseDownloadLocal(firebaseProject)