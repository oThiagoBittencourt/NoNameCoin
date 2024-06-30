from .Connector import Connector
from Controller.DBController import ValidatorDB
from Controller.ValidatorSelector import select_validator
import datetime
import requests

def Transaction(value:float, sender_id:str, sender_balance:float, time:datetime):
    validators = select_validator()
    if validators:
        responses = {}
        for validator in validators:
            user_validator = ValidatorDB.find_validator_by_user(validator)
            response = requests.post('http://' + user_validator.ip + ':' + user_validator.port + '/validador/transaction')
            responses[user_validator.user] = response['response']
            print(response['response'])

def is_rate_limited(sender_id:str, time:datetime):
    return transaction_register_controller(sender_id, time)

def transaction_register_controller(sender_id:str, time:datetime):
    user_requests = Connector.get_user_requests(sender_id)
    
    TIME_WINDOW = 60
    MAX_REQUESTS = 100
    if user_requests:
        recent_requests = [req['timestamp'] for req in user_requests if time - req['timestamp'] < TIME_WINDOW]
        if len(recent_requests) >= MAX_REQUESTS:
            return True
    return False