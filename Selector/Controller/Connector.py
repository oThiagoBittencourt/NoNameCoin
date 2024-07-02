import requests

class Connector:
    def __init__(self):
        self.url = 'http://127.0.0.1:5000'
    
    # BANCO
    def get_user_requests(self, user_id):
        url = f'{self.url}/transacoes/{user_id}'
        response = requests.post(url)
        return response
    
    def update_transaction(self, sender_id, status):
        url = f'{self.url}/transacoes/{sender_id}/{status}'
        requests.post(url)
        return
    
    def register_selector(self, selector_ip, name):
        url = f'{self.url}/seletor/{name}/{selector_ip}'
        requests.post(url)
        return
    
    def edit_status_transaction(self, transaction_id:int, status:int):
        url = f'{self.url}/transacoes/{transaction_id}/{status}'
        requests.post(url)
        return
    
    def ping_validator(self, ip, port):
        try:
            url = f"http://{ip}:{port}/validador/ping"
            response = requests.get(url)
            if response.status_code == 200:
                return True
            return False
        except:
            return False