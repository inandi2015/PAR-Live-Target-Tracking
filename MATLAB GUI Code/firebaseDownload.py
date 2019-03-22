# Requires Python 3.5 or lower version of Python 3

import sys
import csv
import json
import numpy
from firebase import firebase 

class FirebaseDownload:
    ### LOCAL MODULES ###

    def firebaseDownloadLocal(self, firebaseProject):
        result = firebaseProject.get('/DEV', 'SignalData')
            
        print(result['Channel1'])
        print(result['Channel2'])
        print(result['Mode'])
        print(result['PhaseDifference'])
        
        if result['Mode'] == 'Tracking':
            dataOut1 = numpy.asarray(result['Channel1']) # Convert result data from database into an array
            dataOut1 = dataOut1.reshape(len(dataOut1), 1) # Shape data for putting in one column of csv file

            with open("Output1.csv", "w") as f:
                writer = csv.writer(f, dialect='excel', lineterminator = '\n')
                writer.writerows(dataOut1)

            dataOut2 = numpy.asarray(result['Channel2']) # Convert result data from database into an array
            dataOut2 = dataOut2.reshape(len(dataOut2), 1) # Shape data for putting in one column of csv file

            with open("Output2.csv", "w") as f:
                writer = csv.writer(f, dialect='excel', lineterminator = '\n')
                writer.writerows(dataOut2)
            
            # Write to a CSV file here the tracking mode so MATLAB can check it
            with open("OutputStatus.csv", "w") as f:
                writer = csv.writer(f, dialect='excel', lineterminator = '\n')
                writer.writerow([result['Mode']])
        elif result['Mode'] == 'Acquisition':
            # Write to a CSV file here the aquisition mode so MATLAB can check it
            with open("OutputStatus.csv", "w") as f:
                writer = csv.writer(f, dialect='excel', lineterminator = '\n')
                writer.writerow([result['Mode']])
        
# firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# firebaseDownloadRadar(firebaseProject)