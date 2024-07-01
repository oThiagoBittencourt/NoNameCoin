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
    
    def get_all_validators_timeout(self):
        results = self.db.search(self.Validator.sequence >= 5)
        online_validators = [record['user'] for record in results]
        return online_validators
    
    def change_status(self, user:str, status:str):
        self.db.update({'status': status}, self.Validator.user == user)
    
    def update_sequence(self, user:str, RESET_MODE=False):
        result = self.db.search(self.Validator.user == user)
        if result:
            if RESET_MODE:
                self.db.update({'sequence': 0}, self.Validator.user == user)
                return
            sequence = result[0]['sequence']
            self.db.update({'sequence': sequence + 1}, self.Validator.user == user)
        return
    
    def increment_transactions(self, user:str):
        result = self.db.search(self.Validator.user == user)
        if result:
            transactions = result[0]['transactions']
            if (transactions < 9999):
                self.db.update({'transactions': transactions + 1}, self.Validator.user == user)
                return
            flags = result[0]['flags']
            if (flags > 0):
                self.db.update({'transactions': 0, 'flags': flags - 1}, self.Validator.user == user)
                return
            self.db.update({'transactions': 0}, self.Validator.user == user)
        return
    
    def add_flag_validator(self, user:str):
        validator = self.db.search(self.Validator.user == user)
        if validator:
            flags = validator[0]['flags']
            if validator[0]['flags'] > 2:
                bans = validator[0]['bans']
                self.db.update({'flags': 0, 'bans': bans + 1, 'status': 'banned', 'balance': 0}, self.Validator.user == user)
                return
            self.db.update({'flags': flags + 1}, self.Validator.user == user)
        return

    def find_validator_by_user(self, user:str):
        validator = self.db.search(self.Validator.user == user)
        if validator:
            return validator
        return
    
    def update_validator_balance(self, user:str, new_balance:float):
            validator = self.db.search(self.Validator.user == user)
            if validator:
                balance = validator[0]['balance']
                self.db.update({'balance': balance + new_balance}, self.Validator.user == user)
            return

    def remove_validator_by_id(self, user:str):
        self.db.remove(self.Validator.user == user)
    
    def close(self):
        self.db.close()