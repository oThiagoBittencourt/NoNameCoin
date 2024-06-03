from flask import Flask
import os
from .Controller import connector
from app import Services as serv

class App(Flask):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def init_app(self):
        data = {
            "validator_id" : "123",
            "validator_password" : "Gesonel",
            "validator_balance" : 100000.00}
        
        response_register = connector.register_validator(data)
        
        if(response_register.status_code == 200 or response_register.status_code == 201):
            
            ###########         CONNECT         ###########
            
            # response_connect = connector.connect(data)
            # if(response_connect.status_code == 200 or response_connect.status_code == 201):
                # Aqui coloca os elementos daqui de baixo nesse if 
                # só esperar o connect do seletor ser finalizado
                
            ###############################################
            
            os.environ['access_token'] = response_register.json().get('access_token')
            self.config['access_token'] = os.environ.get('access_token')
            serv.register_routes(self)

def create_app():
    app = App(__name__)
    app.init_app()
    return app
        
    