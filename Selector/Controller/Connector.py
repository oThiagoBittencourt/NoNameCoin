import requests

class Connector:
    def __init__(self):
        self.url = 'http://localhost:5002'

    def get_user_requests(self, user_id):
        url = f'{self.url}/transacoes/{user_id}'
        response = requests.post(url)
        return response
    
    def update_transaction(self, sender_id, status):
        url = f'{self.url}/transactions/{sender_id}/{status}'
        response = requests.post(url)
        return