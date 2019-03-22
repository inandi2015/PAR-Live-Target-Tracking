from firebaseDownload import FirebaseDownload
from firebase import firebase

download = FirebaseDownload()
firebaseProject = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/DEV', None)
# Execute function logic here or elsewhere as needed
download.firebaseDownloadLocal(firebaseProject)