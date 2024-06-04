from tinydb import TinyDB, Query

class ValidatorDB:
    def __init__(self, db_path='Selector/TinyDB/validatorDB.json'):
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

class transactionsDB:
    def __init__(self, db_path='Selector/TinyDB/transactionsDB.json'):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.Transaction = Query()

    def get_user_requests(self, user_id):
        """Retorna todas as solicitações do usuário."""
        return self.db.search(self.Transaction.user_id == user_id)

    def filter_recent_requests(self, user_requests, current_time, TIME_WINDOW):
        """Filtra solicitações que estão dentro da janela de tempo."""
        return [req['timestamp'] for req in user_requests if current_time - req['timestamp'] < TIME_WINDOW]

    def update_user_requests(self, user_id, recent_requests, current_time):
        """Atualiza o registro de solicitações do usuário no TinyDB."""
        self.db.remove(self.Transaction.user_id == user_id)
        for timestamp in recent_requests:
            self.db.insert({'user_id': user_id, 'timestamp': timestamp})
        self.db.insert({'user_id': user_id, 'timestamp': current_time})

    def add_user_request(self, user_id, current_time):
        """Adiciona uma nova solicitação para o usuário."""
        self.db.insert({'user_id': user_id, 'timestamp': current_time})
