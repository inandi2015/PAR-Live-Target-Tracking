from firebaseUpload import FirebaseHandshake
from firebase import firebase

firebaseHandshake = FirebaseHandshake()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# Execute function logic here or elsewhere as needed
firebaseHandshake.firebaseUploadStop(firebaseProject)