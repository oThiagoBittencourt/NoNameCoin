import os
import requests


def register_validator(data, ip):
    url = f'{ip}/seletor/register'
    response = requests.post(url, json=data)
    
    return response

def connect(data, ip):
    url = f'{ip}/seletor/connect'
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        os.environ['access_token'] = response.json().get('access_token')
        return response
    else:
        print(f'{response.status_code}')

def time(data, ip):
    url = f'{ip}/seletor/time'
    headers  = {'Authorization': f'Bearer {data}'}
    response = requests.get(url, headers=headers)
    return response

def ratelimited(data, token, ip):
    url = f'{ip}/seletor/ratelimited'
    headers  = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, json=data, headers=headers)
    if response.status_code == 200:
        return 1
    else:
        return 2