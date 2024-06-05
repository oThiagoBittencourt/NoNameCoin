from Controller.DBController import ValidatorDB
from Selector.Controller import TransactionController
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import base64
import os

app = Flask(__name__)
db = ValidatorDB()

# Configuração da chave secreta para assinar os tokens JWT
app.config['JWT_SECRET_KEY'] = base64.b64encode(os.urandom(64)).decode('utf-8')
jwt = JWTManager(app)

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
        client_port = request.environ.get('REMOTE_PORT')

        if not validator_user or not validator_password:
            return jsonify({"msg": "Missing Variables"}), 400
            
        if not db.connect_validator(user=validator_user, password=validator_password, ip=client_ip, port=client_port):
            return jsonify({"msg": "Connection_Error"}), 401

        access_token = create_access_token(identity=validator_user)
        return jsonify(access_token=access_token), 200
    except:
        return jsonify({"msg": "Error!"}), 400

@app.route('/seletor/time', methods=['GET'])
@jwt_required()
def time():
    # Pegar horario do banco
    pass

@app.route('/seletor/ratelimited', methods=['GET'])
@jwt_required()
def ratelimited():
    if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    user_id = request.json.get('user_id', None)

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    if TransactionController.is_rate_limited(user_id):
        return jsonify({'error': 'Too many requests'}), 429
    
    return jsonify({'status': 'request processed'}), 200

###########
# -BANCO- #
###########

@app.route('/seletor/transaction', methods=['POST'])
def transaction():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        transaction_value = request.json.get('transaction_value', None)
        transaction_sender_id = request.json.get('transaction_sender_id', None)
        transaction_sender_balance = request.json.get('transaction_sender_balance', None)
        transaction_time = request.json.get('transaction_time', None)

        if not transaction_sender_id or not transaction_value or not transaction_sender_balance or not transaction_time:
            return jsonify({"msg": "Missing Variables"}), 400
        
        response = TransactionController.Transaction(transaction_value, transaction_sender_id, transaction_sender_balance, transaction_time)

        return jsonify({"response": response}), 200
    except:
        return jsonify({"msg": "Error!"}), 400

if __name__ == '__main__':
    app.run()