from Controller.DBController import ValidatorDB
from Controller import TransactionController
from Controller.Connector import Connector
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import base64
import os
import requests
import datetime

app = Flask(__name__)
db = ValidatorDB()

app.config['JWT_SECRET_KEY'] = base64.b64encode(os.urandom(64)).decode('utf-8')
jwt = JWTManager(app)

####################
# -INITIALIZE APP- #
####################

def initialize_app():
    with app.app_context():
        connector = Connector() 
        connector.register_selector(selector_ip='127.0.0.1:5002', name='PixVulture')

###############
# -VALIDADOR- #
###############

# Rota de login
@app.route('/seletor/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        validator_user = request.json.get('validator_user', None)
        validator_password = request.json.get('validator_password', None)
        validator_balance = request.json.get('validator_balance', None)

        if not validator_user or not validator_password or not validator_balance:
            return jsonify({"msg": "Missing Variables"}), 400
            
        if not db.register_validator(user=validator_user, password=validator_password, balance=validator_balance):
            return jsonify({"msg": "Already_used_user"}), 409
        
        return jsonify({"msg": "Successfully_Registered"}), 200
    except:
            return jsonify({"msg": "Error!"}), 400

@app.route('/seletor/connect', methods=['POST'])
def connect():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        validator_user = request.json.get('validator_user', None)
        validator_password = request.json.get('validator_password', None)
        client_ip = request.remote_addr
        client_port = request.json.get('port', None)

        validator = db.find_validator_by_user(user=validator_user)
        if validator['status'] == 'banned':
            if validator['bans'] == 1:
                value = 100
            if validator['bans'] == 2:
                value = 200 
            if  validator['bans'] == 3:
                return jsonify({"msg": "Banned"}), 430
            return jsonify({"msg": "Banned", 'bans' : validator['bans'], 'value' : value}), 420
        
        if not validator_user or not validator_password:
            return jsonify({"msg": "Missing Variables"}), 400
            
        if not db.connect_validator(user=validator_user, password=validator_password, ip=client_ip, port=client_port):
            return jsonify({"msg": "Connection_Error"}), 401

        access_token = create_access_token(identity=validator_user)
        return jsonify(access_token=access_token), 200
    except:
            return jsonify({"msg": "Error!"}), 400


@app.route('/seletor/unban', methods=['GET'])
def unban():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        validator_user = request.json.get('validator_user', None)
        balance = request.json.get('balance', None)
        value = request.json.get('value', None)
        
        if balance >=  value:
            validator = db.find_validator_by_user(validator_user)
            validator['status'] = 'offline'
            validator['balance'] = value
            return jsonify({"msg": "Unbanned!!"}), 200
        else:
            return jsonify({"msg": "Value less than required!!"}), 401
    except:
            return jsonify({"msg": "Error!"}), 400
    
@app.route('/seletor/time', methods=['GET'])
@jwt_required()
def time():
    try:
        url = 'http://127.0.0.1:5000/hora'
        response = requests.get(url)
        return jsonify({"time": response.json()}), 200
    except:
            return jsonify({"msg": "Error!"}), 400

@app.route('/seletor/ratelimited', methods=['GET'])
@jwt_required()
def ratelimited():
    try:
        if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400

        user_id = request.json.get('sender_id')
        time = request.json.get('time')
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

        if not user_id or not time:
            return jsonify({'error': 'user_id is required'}), 400
        
        if TransactionController.is_rate_limited(user_id, time):
            return jsonify({'error': 'Too many requests'}), 429
        
        return jsonify({'status': 'request processed'}), 200
    except:
        return jsonify({"msg": "Error!"}), 400

###########
# -BANCO- #
###########

@app.route('/transacoes', methods=['POST'])
def transaction():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 450
        
        transaction_id = request.json.get('transaction_id', None)
        transaction_value = request.json.get('transaction_value', None)
        transaction_sender_id = request.json.get('transaction_sender_id', None)
        transaction_sender_balance = request.json.get('transaction_sender_balance', None)
        transaction_time = request.json.get('transaction_time', None)
        last_transaction_time = request.json.get('last_transaction_time', None)
        seletor = request.json.get('seletor', None)

        if not transaction_sender_id or not transaction_value or not transaction_sender_balance or not transaction_time or not last_transaction_time:
            return jsonify({"msg": "Missing Variables"}), 410
        
        response = TransactionController.Transaction(transaction_id, transaction_value, transaction_sender_id, transaction_sender_balance, transaction_time, last_transaction_time, seletor)
        return jsonify({"response": response}), 200
    except:
        return jsonify({"msg": "Error!"}), 400

if __name__ == '__main__':
    initialize_app()
    app.run(port=5002)