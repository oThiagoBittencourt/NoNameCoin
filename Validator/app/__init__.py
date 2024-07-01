
from flask import Flask
import os
from .Controller import Connector
from app import Services
from .Controller.Utils import Utils

class App(Flask):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.url = 'http://localhost:5002'
        self.port = Utils.ramdom_port()

    def init_app(self):
        # data = Utils.create_validator()
        data ={
        'validator_user': 'seilaa',
        'validator_password': 'seila',
        'validator_balance': 600,
        'port' : None
        }
        data['port'] = self.port
        
        response_register = Connector.register_validator(data,self.url)
        
        if(response_register.status_code == 200 or response_register.status_code == 409):    
            response_connect = Connector.connect(data, self.url)
            if response_connect.status_code == 430:
                print('Permanently banned!')
                os._exit(0)
            if response_connect.status_code == 420:
                while(True):
                    print(f'You have been banned {response_connect.json().get('bans')} times.\nDeposit an amount greater than {response_connect.json().get('value')}:')
                    balance = int(input())
                    response_unban = Connector.unban({'balance' : balance, 'value' : response_connect.json().get('value'), 'validator_user' : data['validator_user']}, self.url)
                    if response_unban.status_code == 200:
                        print(response_unban.json().get('msg'))
                        response_connect = Connector.connect(data, self.url)
                        break
                    print(response_unban.json().get('msg'))
            if(response_connect.status_code == 200 or response_connect.status_code == 409):
                environ_name = data['validator_user'] + '_access_token'
                os.environ[environ_name] = response_connect.json().get('access_token')
                self.config['access_token'] = os.environ.get(environ_name)
                Services.register_routes(self)
                
def create_app():
    app = App(__name__)
    app.init_app()
    app.run(debug=True, use_reloader=False, port=app.port)
    return app
