import datetime
from . import Connector
import os

url = 'http://localhost:5002'

def verify_balance(balance, value):
    if(balance < value + (value * (1.5 / 100))):
        return 2
    return 1

def verify_transaction_time(transaction_time, last_transaction_time, environ_name):
    response = Connector.time(os.environ.get(environ_name), url)
    if response.status_code != 200:
        return 2
    current_datetime = datetime.datetime.strptime(response.json().get('time'), "%Y-%m-%d %H:%M:%S.%f")
    transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
    last_transaction_time = datetime.datetime.strptime(last_transaction_time, "%Y-%m-%d %H:%M:%S.%f")
    current_datetime = current_datetime.timestamp()
    transaction_time = transaction_time.timestamp()
    last_transaction_time = last_transaction_time.timestamp()
    if((transaction_time > current_datetime) or (transaction_time < last_transaction_time)):
        return 2
    return 1

def verify_ratelimited(transaction_sender_id, transaction_time, environ_name):
    rate_limit = Connector.ratelimited({'sender_id' : transaction_sender_id, 'time' : transaction_time}, os.environ.get(environ_name), url)
    return rate_limit

def Validator(data):
    environ_name = data['validator'] + '_access_token'
    status_balance = verify_balance(data['sender_balance'], data['value'])
    status_transaction_time = verify_transaction_time(data['time'], data['last_time'], environ_name)
    status_ratelimited = verify_ratelimited(data['sender_id'], data['time'], environ_name)
    if(status_balance == 2 or status_transaction_time == 2 or status_ratelimited == 2):
        return 2
    return 1