import random
from firebase import firebase
from firebase_admin import db
import json

data = {'url': 'test', 'address': 'test', 'name': 'name'}
sent = json.dumps(data)

firebase = firebase.FirebaseApplication('https://par-live-target-tracking.firebaseio.com/test', None)

firebase.post('/test', sent)

result = firebase.get('/test', None);
print(result['name'])

# result = firebase.post('/test',{'ID':random.randrange(100000, 999999, 6)})