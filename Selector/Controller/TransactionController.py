from .Connector import Connector
from Controller.DBController import ValidatorDB
from Controller.ValidatorSelector import select_validator
import datetime
import requests

def Transaction(transaction_id:int, value:float, sender_id:str, sender_balance:float, time:datetime, seletor:dict):
    response = 0
    validators = select_validator()
    if validators:
        validator_responses = {}
        for validator in validators:
            user_validator = ValidatorDB.find_validator_by_user(validator)
            json = {'value': value, 'sender_id': sender_id, 'sender_balance': sender_balance, 'time': time}
            validator_response_transaction = Connector.request_transaction(f"http://{user_validator['ip']}:{user_validator['port']}", json)
            validator_responses[validator] = validator_response_transaction.json().get('response')
        result, users = check_users(validator_responses)
        response = result
        if (response is 1):
            selector_profit = value * (1/100)
            validators_profit = value * (0.5/100)
            share_profits(selector_profit, validators_profit, users, seletor)
        for validator in validators:
            if validator not in users:
                ValidatorDB.add_flag_validator(validator)
            else:
                ValidatorDB.increment_transactions(validator)
        Connector.edit_status_transaction(transaction_id=transaction_id, status=response)
    return response

def check_users(dictionary:dict):
    count = {0: [], 1: [], 2: []}
    for user, number in dictionary.items():
        count[number].append(user)
    for number, users in count.items():
        if len(users) > len(dictionary) / 2:
            return number, users
    return 2, list(dictionary.keys())

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

def share_profits(selector_profit: float, validators_profit: float, validators, seletor):
    profit = validators_profit / len(validators)
    for validator in validators:
        ValidatorDB.update_validator_balance(user=validator, new_balance=profit)
    selector_profit = seletor['qtdMoeda'] + selector_profit
    url_seletor = f'http://127.0.0.1:5000/seletor/{seletor['id']}/{seletor['nome']}/{seletor['ip']}/{selector_profit}'
    requests.post(url_seletor)
    return