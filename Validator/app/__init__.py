from flask import Flask
import os
from .Controller import connector
from app import Services
import time
import threading
from datetime import datetime, timedelta, timezone

BRST = timezone(timedelta(hours=-3))  # Set standard time

class App(Flask):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def init_app(self):
        data = {
            "validator_user" : "123",
            "validator_password" : "Gesonel",
            "validator_balance" : 100000.00
        }
            
        response_register = connector.register_validator(data)
        
        if(response_register.status_code == 200 or response_register.status_code == 409):    
            response_connect = connector.connect(data)
            
            if(response_connect.status_code == 200 or response_connect.status_code == 409):
                os.environ['access_token'] = response_connect.json().get('access_token')
                self.config['access_token'] = os.environ.get('access_token')
                Services.register_routes(self)
                
    def sync_time(self):
        while True:
            try:
                response = connector.time()
                if response.status_code == 200:
                    server_time = datetime.fromisoformat(response.json().get('time'))
                    server_time = datetime.fromisoformat(server_time)
                    local_time = server_time.astimezone(BRST)
                    
                    current_local_time = datetime.now(BRST)
                    print(f"Horário local atual antes da mudança: {current_local_time}")
                    
                    # Imprime o horário recebido do servidor
                    print(f"Horário recebido do servidor: {local_time}")

                    # Simulando a mudança de horário imprimindo o novo horário
                    print(f"Horário local atualizado para: {local_time}")
                    
            except Exception as e:
                print(f"Erro ao obter o horário do servidor: {e}")
            
            time.sleep(60)
    thread = threading.Thread(target=sync_time)
    thread.daemon = True
    thread.start()


def create_app():
    app = App(__name__)
    app.init_app()
    return app


        
    