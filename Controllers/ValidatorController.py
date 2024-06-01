import json
import datetime
import os
import requests

#verificação de saldo da conta
def verify_balance(balance, value, tax):
    #verifica se o saldo da conta tem dinheiro para ser enviado
    if(balance < value + (value * (tax / 100))):
        return 2
    return 1

#verificação do tempo da transação
def verify_transaction_time(transaction_time, last_transaction_time):
    #instancia uma variavel que tem o valor do timestamp atual
    current_datetime = datetime.datetime.now().timestamp()
    #verifica se o timestamp da transação é maior que o timestamp atual e se o timestamp da transação é menor que o timestamp da ultima transação
    #caso de negativo para essas verificações, a transação está apta a continuar
    if((transaction_time > current_datetime) or (transaction_time < last_transaction_time)):
        return 2
    return 1


def Validator(data):
    #transforma o JSON em dicionario para trabalhar melhor com as variaveis
    data = json.loads(data)
    #chama a verificação do saldo
    status_balance = verify_balance(data['account_balance'], data['value'], data['taxes'])
    #chama a verificação do timestamp da transação
    status_transaction_time = verify_transaction_time(data['transaction_time'], data['last_transaction_time'])
    #verifica se todas as validações foram concluidas com exito
    if(status_balance == 2 or status_transaction_time == 2):
        return 2
    


# JSON HIPOTÉTICO

#colocando os valores em um dicionario
transaction_time = datetime.datetime.now().timestamp()
data =  { 
    "validator_id": 0,
    "id_account":1, 
    "account_balance":3000, 
    "value":300, 
    "id_receiver":12, 
    "transaction_time":transaction_time,
    "last_transaction_time": 1213141.22,
    "taxes": 5,
    }

#transformar dicionario em jsco
data = json.dumps(data)

#chama a função do validador
Validator(data)

def register_validator():
    data = {
        'validator_id' : 1,
        'validator_balance' : 3000}
    
    url = 'http://localhost:5000/selector/register'
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        os.environ['access_token'] = response['access_token']
        print()
    else:
        print(f'{response.status_code} - {response['msg']}')
    


