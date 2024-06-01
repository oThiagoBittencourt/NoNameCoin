from Controller.DBController import Database
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
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    validator_id = request.json.get('validator_id', None)
    validator_balance = request.json.get('validator_balance', None)
    client_ip = request.remote_addr
    client_port = request.environ.get('REMOTE_PORT')

    if not validator_id or not validator_balance:
        return jsonify({"msg": "Missing Variables"}), 400
        
    if not db.insert_validator(id=validator_id, ip=client_ip, port=client_port, balance=validator_balance):
        return jsonify({"msg": "Already_used_id"}), 400

    access_token = create_access_token(identity=validator_id)
    return jsonify(access_token=access_token), 200
# Rota protegida
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Obter a identidade do usuário atual (neste caso, o nome de usuário)
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run()
