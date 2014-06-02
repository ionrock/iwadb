import json

import requests

url = 'http://localhost:8080/foo'
doc = {'hello': 'world'}

requests.put(url, headers={'Content-Type': 'application/json'},
             data=json.dumps(doc))
print(requests.get(url).json())
