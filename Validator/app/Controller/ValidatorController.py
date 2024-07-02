import datetime
from . import Connector
import os

url = 'http://localhost:5002'

#verificação de saldo da conta
def verify_balance(balance, value):
    #verifica se o saldo da conta tem dinheiro para ser enviado
    if(balance < value + (value * (1.5 / 100))):
        return 2
    return 1

#verificação do tempo da transação
def verify_transaction_time(transaction_time, last_transaction_time, environ_name):
    #instancia uma variavel que tem o valor do timestamp atual
    response = Connector.time(os.environ.get(environ_name), url)
    if response.status_code != 200:
        return 2
    #pega os dados que estão em string e converte em datetime
    current_datetime = datetime.datetime.strptime(response.json().get('time'), "%Y-%m-%d %H:%M:%S.%f")
    transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S.%f")
    last_transaction_time = datetime.datetime.strptime(last_transaction_time, "%Y-%m-%d %H:%M:%S.%f")
    #converte em timestamp
    current_datetime = current_datetime.timestamp()
    transaction_time = transaction_time.timestamp()
    last_transaction_time = last_transaction_time.timestamp()
    #verifica se o timestamp da transação é maior que o timestamp atual e se o timestamp da transação é menor que o timestamp da ultima transação
    #caso de negativo para essas verificações, a transação está apta a continuar
    if((transaction_time > current_datetime) or (transaction_time < last_transaction_time)):
        return 2
    return 1

def verify_ratelimited(transaction_sender_id, transaction_time, environ_name):
    rate_limit = Connector.ratelimited({'sender_id' : transaction_sender_id, 'time' : transaction_time}, os.environ.get(environ_name), url)
    return rate_limit

def Validator(data):
    print(type(data)) ###
    environ_name = data['validator'] + '_access_token'
    #chama a verificação do saldo
    status_balance = verify_balance(data['sender_balance'], data['value'])
    #chama a verificação do timestamp da transação
    status_transaction_time = verify_transaction_time(data['time'], data['last_time'], environ_name)
    #verifica se todas as validações foram concluidas com exito
    status_ratelimited = verify_ratelimited(data['sender_id'], data['time'], environ_name)
    if(status_balance == 2 or status_transaction_time == 2 or status_ratelimited == 2):
        return 2
    return 1

# {'value': value, 'sender_id': sender_id, 'sender_balance': sender_balance, 'time': time, 'last_time': last_time, 'validator': validator}