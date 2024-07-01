from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: str
    qtdMoeda: float

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)

@dataclass
class Seletor(db.Model):
    id: int
    nome: str
    ip: str
    qtdMoeda: float
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Float, unique=False, nullable=False)
@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: float
    horario : datetime
    status: int
    
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Float, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False, default=lambda: datetime.now())
    status = db.Column(db.Integer, unique=False, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return jsonify(['API sem interface do banco!'])

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
@app.route('/cliente/<string:nome>/<string:senha>/<float:qtdMoeda>', methods = ['POST'])
def InserirCliente(nome, senha, qtdMoeda):
    if request.method=='POST' and nome != '' and senha != '' and qtdMoeda >= 0.0:
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
        return jsonify(['Method Not Allowed']), 400

# Atualiza informações sobre o cliente
@app.route('/cliente/<int:id>/<float:qtdMoeda>', methods=["POST"])
def EditarCliente(id, qtdMoeda):
    if request.method=='POST':
        try:
            cliente = Cliente.query.filter_by(id=id).first()
            cliente.qtdMoeda = qtdMoeda
            db.session.commit()
            return jsonify(['Alteração feita com sucesso'])
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)

    else:
        return jsonify(['Method Not Allowed']), 400

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
        return jsonify(['Method Not Allowed']), 400

#################
#   -Seletor-   #
#################

# Devolve todos os seletores
@app.route('/seletor', methods = ['GET'])
def ListarSeletor():
    if(request.method == 'GET'):
        seletores = Seletor.query.all()
        return jsonify(seletores)  

# Registra um seletor <-- !!!
@app.route('/seletor/<string:nome>/<string:ip>', methods = ['POST'])
def InserirSeletor(nome, ip):
    if request.method=='POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed']), 400

# Devolve um seletor pelo ID
@app.route('/seletor/<int:id>', methods = ['GET'])
def UmSeletor(id):
    if(request.method == 'GET'):
        seletor = Seletor.query.get(id)
        return jsonify(seletor)
    else:
        return jsonify(['Method Not Allowed']), 400

# Atualizar dados de um seletor
@app.route('/seletor/<int:id>/<string:nome>/<string:ip>/<float:qtdMoeda>', methods=["POST"])
def EditarSeletor(id, nome, ip, qtdMoeda):
    if request.method=='POST':
        try:
            varNome = nome
            varIp = ip
            varQtdMoeda = qtdMoeda
            seletor = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            seletor.nome = varNome
            seletor.ip = varIp
            seletor.qtdMoeda = varQtdMoeda
            db.session.commit()
            return jsonify(seletor)
        except Exception as e:
            data={
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed']), 400

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
        return jsonify(['Method Not Allowed']), 400

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

# Cria uma transação e envia ela pra pros seletores <-- !!!
@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods = ['POST'])
def CriaTransacao(rem, reb, valor):
    if request.method=='POST':
        time = datetime.now()
        objeto = Transacao(remetente=rem, recebedor=reb,valor=valor,status=0,horario=time)
        db.session.add(objeto)
        db.session.commit()
        remetente = Cliente.query.get(id)
        seletores = Seletor.query.all()
        for seletor in seletores:
            url = 'http://' + seletor.ip + '/transacoes/'
            objetos_transacao = {'transaction_id': objeto.id,'transaction_value': valor, 'transaction_sender_id': rem, 'transaction_sender_balance': remetente.qtdMoeda, 'transaction_time': time, 'seletor': {'ip':seletor.ip, 'nome': seletor.nome, 'id': seletor.id, 'qtdMoeda': seletor.qtdMoeda}}
            requests.post(url, data=jsonify(objetos_transacao))
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed']), 400

# Retorna todas as transações de um usuario pelo ID <-- !!!
@app.route('/transacoes/<int:id>', methods = ['GET'])
def UmaTransacao(id):
    if(request.method == 'GET'):
        objeto = Transacao.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed']), 400

# Atualiza os dados de uma transação pelo ID <-- !!!
@app.route('/transacoes/<int:id>/<int:status>', methods=["POST"])
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
        return jsonify(['Method Not Allowed']), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
    
app.run(host='0.0.0.0', debug=True)