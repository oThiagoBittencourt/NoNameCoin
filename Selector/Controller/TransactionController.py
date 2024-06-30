from .Connector import Connector
from Controller.DBController import ValidatorDB
from Controller.ValidatorSelector import select_validator
import datetime
import requests

def Transaction(value:float, sender_id:str, sender_balance:float, time:datetime, seletor:dict):
    response = 0
    validators = select_validator()
    if validators:
        validator_responses = {}
        for validator in validators:
            user_validator = ValidatorDB.find_validator_by_user(validator)
            validator_response = requests.post('http://' + user_validator.ip + ':' + user_validator.port + '/validador/transaction')
            validator_responses[validator] = validator_response['response']
        # {Thiago: 1, Gabriel: 1, Gal: 2}
        result, users = check_users(validator_responses)
        response = result
        if (response is 1):
            # Função do Gabriel
            pass
        for validator in validators:
            if validator not in users:
                ValidatorDB.add_flag_validator(validator)
            else:
                ValidatorDB.increment_transactions(validator)
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
    for validator in validators:
        profit = validators_profit / len(validators)
        ValidatorDB.update_validator_balance(user=validator, new_balance=profit)
    selector_profit = seletor['qtdMoeda'] + selector_profit
    url_seletor = f'/seletor/{seletor['id']}/{seletor['nome']}/{seletor['ip']}/{selector_profit}'
    requests.post(url_seletor)

    pass