from firebaseUpload import FirebaseUpload
from firebase import firebase
import sys

upload = FirebaseUpload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# Execute function logic here or elsewhere as needed
upload.firebaseUploadLocal(firebaseProject, sys.argv[1])