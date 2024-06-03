from Controller.DBController import Database
from Controller import Controller
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import base64
import os

app = Flask(__name__)
db = Database()

# Configuração da chave secreta para assinar os tokens JWT
app.config['JWT_SECRET_KEY'] = base64.b64encode(os.urandom(64)).decode('utf-8')
jwt = JWTManager(app)

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
            return jsonify({"msg": "Already_used_user"}), 400
        
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
            return jsonify({"msg": "Connection_Error"}), 400

        access_token = create_access_token(identity=validator_user)
        return jsonify(access_token=access_token), 200
    except:
        return jsonify({"msg": "Error!"}), 400

@app.route('/seletor/transaction', methods=['POST'])
def transaction():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        transaction_value = request.json.get('transaction_value', None)
        transaction_sender_balance = request.json.get('transaction_sender_balance', None)
        transaction_time = request.json.get('transaction_time', None)

        if not transaction_value or not transaction_sender_balance or not transaction_time:
            return jsonify({"msg": "Missing Variables"}), 400
        
        response = Controller.Transaction(transaction_value, transaction_sender_balance, transaction_time)

        return jsonify({"response": response}), 200
    except:
        return jsonify({"msg": "Error!"}), 400

##################################################################################################################

# Rota protegida
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Obter a identidade do usuário atual (neste caso, o nome de usuário)
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run()