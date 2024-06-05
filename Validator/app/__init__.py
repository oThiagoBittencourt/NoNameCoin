
from flask import Flask
from dateutil import parser
import os
from .Controller import connector, Utils
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
                response = connector.time(self.config.get('access_token'))
                if response.status_code == 200:
                    server_time_str = response.json().get('time')
                    server_time = datetime.fromisoformat(server_time_str)
                    local_time = server_time.astimezone(BRST)

                    dt = parser.parse(str(local_time))
                    print(f"\nOld time:      {local_time}")
                    print(dt)

                    print(type(dt))
                    new_time_struct = dt.timetuple()
                    time.mktime(new_time_struct)
                    print(datetime.now(BRST))
                    Utils.update_server_time(local_time)

            except Exception as e:
                print(f"Error getting server time: {e}\n")
            time.sleep(60)

    def start_sync_time_thread(self):
        thread = threading.Thread(target=self.sync_time)
        thread.daemon = True
        thread.start()

def create_app():
    app = App(__name__)
    app.init_app()
    app.start_sync_time_thread()
    return app


        
    