import requests
import json
r = requests.get('http://127.0.0.1:9000/mine')
if r.status_code == 200:
    print(r.json())

neighbor = {
    "neighbors": [
        'http://127.0.0.1:9003',
        'http://127.0.0.1:9005'
    ]
}

print(1)
r2 = requests.post('http://127.0.0.1:9000/neighbor/add', json=neighbor)
print(2)

if r2.status_code == 201:
    print(r2.json())
