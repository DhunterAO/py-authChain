import requests
import json


responce = requests.get('http://127.0.0.1:5000/chain')

responce = requests.post('http://127.0.0.1:5000/transactions/new',json={'sender':'a','recipient':'b','amount':1})
