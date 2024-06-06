
from flask import Flask
import os
from .Controller import Connector
from app import Services
from datetime import datetime, timedelta, timezone

BRST = timezone(timedelta(hours=-3))  # Set standard time

class App(Flask):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.url = 'http://localhost:5002'

    def init_app(self):
        data = {
            "validator_user" : "123",
            "validator_password" : "Gesonel",
            "validator_balance" : 100000.00
        }
            
        response_register = Connector.register_validator(data,self.url)
        
        if(response_register.status_code == 200 or response_register.status_code == 409):    
            response_connect = Connector.connect(data, self.url)
            
            if(response_connect.status_code == 200 or response_connect.status_code == 409):
                os.environ['access_token'] = response_connect.json().get('access_token')
                self.config['access_token'] = os.environ.get('access_token')
                Services.register_routes(self)
                
def create_app():
    app = App(__name__)
    app.init_app()
    return app


        
    