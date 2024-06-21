import requests

class Connector:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000'

    def get_user_requests(self, user_id):
        url = f'{self.url}/transacoes/{user_id}'
        response = requests.post(url)
        return response
    
    def update_transaction(self, sender_id, status):
        url = f'{self.url}/transacoes/{sender_id}/{status}'
        response = requests.post(url)
        return
    
    def register_selector(self, selector_ip, name):
        url = f'{self.url}/seletor/{name}/{selector_ip}'
        response = requests.post(url)
        return
        
