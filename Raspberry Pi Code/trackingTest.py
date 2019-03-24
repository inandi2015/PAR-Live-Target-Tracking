import subprocess
from firebaseUpload import FirebaseUpload
from firebaseDownload import FirebaseDownload
from firebase import firebase
import time

upload = FirebaseUpload()
download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)

upload.firebaseUploadTracking(firebaseProject)
