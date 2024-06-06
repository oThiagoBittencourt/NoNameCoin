from tinydb import TinyDB, Query

class ValidatorDB:
    def __init__(self, db_path='Selector/TinyDB/validatorDB.json'):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.Validator = Query()
    
    def register_validator(self, user:str, password:str, balance:float):
        if (self.db.search(self.Validator.user == user)):
            return False
        self.db.insert({'user': user, 'password': password, 'balance': balance, 'ip': None, 'port': None, 'flags': 0, 'bans': 0, 'sequence': 0, 'transactions': 0, 'status': 'offline'})
        return True
    
    def connect_validator(self, user:str, password:str, ip:str, port:int):
        validator = self.db.search(self.Validator.user == user)
        if validator:
            if validator[0]['password'] != password or validator[0]['status'] == 'banned':
                return False
            self.db.update({'ip': ip, 'port': port, 'status': 'online'}, self.Validator.user == user)
            return True
        return False
    
    def get_all_validators_online(self):
        results = self.db.search((self.Validator.status == 'online') & (self.Validator.sequence < 5))
        online_validators = {record['user']: {'balance': record['balance'], 'flags': record['flags']} for record in results}
        return online_validators
    
    def find_validator_by_id(self, user:str):
        return self.db.search(self.Validator.user == user)
    
    def update_validator(self, user:str, password:str, ip:str, port:int, balance:float, flags:int, bans:int, status:str):
        self.db.update({'user': user, 'password': password, 'balance': balance,'ip': ip, 'port': port, 'flags': flags, 'bans': bans, 'status': status}, self.Validator.user == user)

    def remove_validator_by_id(self, user:str):
        self.db.remove(self.Validator.user == user)
    
    def close(self):
        self.db.close()

"""
class transactionsDB:
    def get_user_requests(self, user_id):
        return self.db.search(self.Transaction.user_id == user_id)

    def filter_recent_requests(self, user_requests, current_time, TIME_WINDOW):
        return [req['timestamp'] for req in user_requests if current_time - req['timestamp'] < TIME_WINDOW]

    def update_user_requests(self, user_id, recent_requests, current_time):
        self.db.remove(self.Transaction.user_id == user_id)
        for timestamp in recent_requests:
            self.db.insert({'user_id': user_id, 'timestamp': timestamp})
        self.db.insert({'user_id': user_id, 'timestamp': current_time})

    def add_user_request(self, user_id, current_time):
        self.db.insert({'user_id': user_id, 'timestamp': current_time})
"""