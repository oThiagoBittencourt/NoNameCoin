from flask import Flask, jsonify, request
from Controller import ValidatorController

def register_routes(app:Flask):
    @app.route('/validador/transaction', methods=['POST'])
    def transaction():
        try:
            if not request.is_json:
                return jsonify({"response": 0, "msg": "Missing JSON in request"}), 400
            data = request.get_json()
            response = ValidatorController.Validator(data)
            return jsonify({"response": response, "msg": "Transaction Processed Successfully"}), 200
        except:
            return jsonify({"response": 0, "msg": "Error!"}), 400
        
    @app.route('/validador/ping', methods=['GET'])
    def ping():
        return jsonify({"status": "online"}), 200
