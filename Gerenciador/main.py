from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import json
  
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: str
    qtdMoeda: int
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Integer, unique=False, nullable=False)

class Seletor(db.Model):
    id: int
    nome: str
    ip: str
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario: datetime
    status: int
    
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False, default=lambda: datetime.now())
    status = db.Column(db.Integer, unique=False, nullable=False)


#@app.before_first_request
#def create_tables():
#    db.create_all()

@app.route("/")
def index():
    return render_template('api.html')

##################
#   -Clientes-   #
##################

# Volta todos os clientes
@app.route('/cliente', methods = ['GET'])
def ListarCliente():
    if(request.method == 'GET'):
        clientes = Cliente.query.all()
        return jsonify(clientes)  

# Inserir cliente no BD
@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoeda>', methods = ['POST'])
def InserirCliente(nome, senha, qtdMoeda):
    if request.method=='POST' and nome != '' and senha != '' and qtdMoeda >= 0:
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed']), 400

# Volta um cliente pelo ID
@app.route('/cliente/<int:id>', methods = ['GET'])
def UmCliente(id):
    if(request.method == 'GET'):
        objeto = Cliente.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

# Atualiza informações sobre o cliente
@app.route('/cliente/<int:id>/<int:qtdMoeda>', methods=["POST"])
def EditarCliente(id, qtdMoeda):
    if request.method=='POST':
        try:
            cliente = Cliente.query.filter_by(id=id).first()
            db.session.commit()
            cliente.qtdMoeda = qtdMoeda
            db.session.commit()
            return jsonify(cliente)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

# Apaga cliente pelo ID
@app.route('/cliente/<int:id>', methods = ['DELETE'])
def ApagarCliente(id):
    if(request.method == 'DELETE'):
        objeto = Cliente.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

#################
#   -Seletor-   #
#################

# Devolve todos os seletores
@app.route('/seletor', methods = ['GET'])
def ListarSeletor():
    if(request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)

# Registra um seletor <-- !!!
@app.route('/seletor/<string:nome>/<string:ip>', methods = ['POST'])
def InserirSeletor(nome, ip):
    if request.method=='POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

# Devolve um seletor pelo ID
@app.route('/seletor/<int:id>', methods = ['GET'])
def UmSeletor(id):
    if(request.method == 'GET'):
        produto = Seletor.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])

# Atualizar dados de um seletor
@app.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=["POST"])
def EditarSeletor(id, nome, ip):
    if request.method=='POST':
        try:
            varNome = nome
            varIp = ip
            validador = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            validador.nome = varNome
            validador.ip = varIp
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

# Delete um seletor
@app.route('/seletor/<int:id>', methods = ['DELETE'])
def ApagarSeletor(id):
    if(request.method == 'DELETE'):
        objeto = Seletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data={
            "message": "Validador Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

##############
#   -Hora-   #
##############

# Devolve a hora <-- !!!
@app.route('/hora', methods = ['GET'])
def horario():
    if(request.method == 'GET'):
        objeto = datetime.now()
        return jsonify(objeto)

####################
#   -Transações-   #
####################

# Retorna todas as transações <-- !!!
@app.route('/transacoes', methods = ['GET'])
def ListarTransacoes():
    if(request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)

# Retorna todas as transações de um usuario específico <-- !!!
@app.route('/transacoes/<int:remetente_id>', methods=['GET'])
def TransacoesPorRemetente(remetente_id):
    if request.method == 'GET':
        transacoes = Transacao.query.filter_by(remetente=remetente_id).all()
        if not transacoes:
            return jsonify({"error": "Nenhuma transação encontrada para este remetente"}), 404
        return jsonify([transacao.to_dict() for transacao in transacoes])
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

# Cria uma transação e envia ela pra pros seletores <-- !!!
@app.route('/transacoes/<int:remetente>/<int:recebedor>/<int:valor>', methods = ['POST'])
def CriaTransacao(remetente, recebedor, valor):
    if request.method=='POST':
        objeto = Transacao(remetente=remetente, recebedor=recebedor,valor=valor,status=0)
        db.session.add(objeto)
        db.session.commit()
        
        objeto_json = {
            'id': objeto.id,
            'remetente': objeto.remetente,
            'recebedor': objeto.recebedor,
            'valor': objeto.valor,
            'horario': objeto.horario,
            'status': objeto.status
        }
  
        seletores = Seletor.query.all()
        for i in seletores:
            url = seletores[i].ip + '/transacao/'
            request.post(url, data=jsonify(objeto_json))
		
        return jsonify(objeto_json)
    else:
        return jsonify(['Method Not Allowed'])

# Retorna todas as transações de um usuario pelo ID <-- !!!
@app.route('/transacoes/<int:id>', methods = ['GET'])
def UmaTransacao(id):
    if(request.method == 'GET'):
        objeto = Transacao.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

# Atualiza os dados de uma transação pelo ID <-- !!!
@app.route('/transactions/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    if request.method=='POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data={
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
    
app.run(host='0.0.0.0', debug=True, port=5002)