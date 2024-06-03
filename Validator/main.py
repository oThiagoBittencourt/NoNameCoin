import connector
from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from Services import register_routes
        register_routes(app=app)
        return app

def start_app(app:Flask):
    app.run(debug=True)

app = create_app()
def main():
    data = {
        "validator_id" : "11111",
        "validator_password" : "Gesonel",
        "validator_balance" : 100000.00}
    
    register_verify = connector.register_validator(data)
    if(register_verify.status_code == 200 or register_verify.status_code == 201):
        # register_connection = connector.connect(data)
        # if(register_connection == 200 or register_connection == 201):
        print('foi')
        start_app(app)
        
main()
