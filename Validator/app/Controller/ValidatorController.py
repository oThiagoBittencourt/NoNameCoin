import datetime
from . import Connector
import os

#verificação de saldo da conta
def verify_balance(balance, value, tax):
    #verifica se o saldo da conta tem dinheiro para ser enviado
    if(balance < value + (value * (tax / 100))):
        return 2
    return 1

#verificação do tempo da transação
def verify_transaction_time(transaction_time, last_transaction_time):
    #instancia uma variavel que tem o valor do timestamp atual
    response = Connector.time(os.environ.get('access_token'))
    if response.status_code != 200:
        return 2
    #pega os dados que estão em string e converte em datetime
    current_datetime = datetime.datetime.strptime(response.json().get('time'), "%a, %d %b %Y %H:%M:%S %Z")
    transaction_time = datetime.datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
    last_transaction_time = datetime.datetime.strptime(last_transaction_time, "%Y-%m-%d %H:%M:%S")
    #converte em timestamp
    current_datetime = current_datetime.timestamp()
    transaction_time = transaction_time.timestamp()
    last_transaction_time = last_transaction_time.timestamp()
    #verifica se o timestamp da transação é maior que o timestamp atual e se o timestamp da transação é menor que o timestamp da ultima transação
    #caso de negativo para essas verificações, a transação está apta a continuar
    if((transaction_time > current_datetime) or (transaction_time < last_transaction_time)):
        return 2
    return 1

def verify_ratelimited(user_id, ):
    rate_limit = Connector.ratelimited({'user_id' : user_id}, os.environ.get('access_token'))
    return rate_limit

def Validator(data):
    #chama a verificação do saldo
    status_balance = verify_balance(data['account_balance'], data['value'], data['taxes'])
    #chama a verificação do timestamp da transação
    status_transaction_time = verify_transaction_time(data['transaction_time'], data['last_transaction_time'])
    #verifica se todas as validações foram concluidas com exito
    status_ratelimited = verify_ratelimited(data['user_id'])
    if(status_balance == 2 or status_transaction_time == 2 or status_ratelimited == 2):
        return 2
    return 1