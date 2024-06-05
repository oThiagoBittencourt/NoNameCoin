import os
import requests

def register_validator(data):
    url = 'http://localhost:5000/seletor/register'
    response = requests.post(url, json=data)
    
    return response

def connect(data):
    url = 'http://localhost:5000/seletor/connect'
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        os.environ['access_token'] = response.json().get('access_token')
        return response
    else:
        print(f'{response.status_code}')

def time(data):
    url = 'http://localhost:5000/seletor/time'
    headers  = {'Authorization': f'Bearer {data}'}
    response = requests.get(url, headers=headers)
    return response

def ratelimited(data):
    url = 'http://localhost:5000/seletor/ratelimited'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return 1
    else:
        return 2