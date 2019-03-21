from firebaseDownload import FirebaseDownload
from firebase import firebase

upload = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# Execute function logic here or elsewhere as needed
upload.firebaseDownloadLocal(firebaseProject)