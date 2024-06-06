from .Connector import Connector
from Controller.ValidatorSelector import select_validator
import datetime
import requests

def Transaction(value:float, sender_id:str, sender_balance:float, time:datetime):
    validators = select_validator()
    response = 1

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