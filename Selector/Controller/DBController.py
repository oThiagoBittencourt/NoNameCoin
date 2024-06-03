from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='Selector/TinyDB/db.json'):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.Validator = Query()
    
    def register_validator(self, user:str, password:str, balance:float):
        if (self.db.search(self.Validator.user == user)):
            return False
        self.db.insert({'user': user, 'password': password, 'balance': balance, 'ip': None, 'port': None, 'flags': 0, 'bans': 0, 'status': 'offline'})
        return True
    
    def connect_validator(self, user:str, password:str, ip:str, port:int):
        validator = self.db.search(self.Validator.user == user)
        if validator:
            if validator[0]['password'] != password or validator[0]['status'] == 'banned':
                return False
            self.db.update({'ip': ip, 'port': port}, self.Validator.user == user)
            return True
        return False
    
    def find_validator_by_id(self, user:str):
        return self.db.search(self.Validator.user == user)
    
    def update_validator(self, user:str, password:str, ip:str, port:int, balance:float, flags:int, bans:int, status:str):
        self.db.update({'user': user, 'password': password, 'balance': balance,'ip': ip, 'port': port, 'flags': flags, 'bans': bans, 'status': status}, self.Validator.user == user)

    def remove_validator_by_id(self, user:str):
        self.db.remove(self.Validator.user == user)
    
    def close(self):
        self.db.close()
