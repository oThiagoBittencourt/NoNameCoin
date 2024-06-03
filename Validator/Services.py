from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import base64
import os

#receber e mudar horario
#esperar atividades do seletor


def register_routes(app:Flask):
    @app.route('/validator/await_activity', methods=['POST'])
    def await_activity():
        return 0
