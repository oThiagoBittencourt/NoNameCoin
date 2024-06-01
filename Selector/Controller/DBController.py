from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='Selector/TinyDB/db.json'):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.Validator = Query()
    
    def insert_validator(self, id:str, ip:str, port:str, balance:float):
        if (self.db.search(self.Validator.id == id)):
            return False
        self.db.insert({'id': id, 'ip': ip, 'port': port, 'balance': balance, 'flags': 0, 'bans': 0, 'status': 'online'})
        return True
    
    def find_validator_by_id(self, id):
        return self.db.search(self.Validator.id == id)
    
    def update_validator(self, id:str, ip:str, port:str, balance:float):
        self.db.update({'id': id, 'ip': ip, 'port': port, 'balance': balance, 'flags': 0, 'bans': 0, 'status': 'online'}, self.Validator.id == id)
    
    def remove_validator_by_id(self, id):
        self.db.remove(self.Validator.id == id)
    
    def close(self):
        self.db.close()
