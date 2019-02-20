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

#result = firebase.get('/test/test', None, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# result = firebase.get('/test/test', None)
# print(result)

# result = firebase.get('/test/test', None, params={'url': 'test2'}, headers={},connection={})
#result = firebase.get('/test', 'test')
#print(result)

#firebase.delete('/test', 'test')  

# result = firebase.post('/test',{'ID':random.randrange(100000, 999999, 6)})