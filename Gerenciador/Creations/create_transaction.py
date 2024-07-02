import requests
import random

endpoint_clientes = 'http://localhost:5000/cliente'
endpoint_transacoes = 'http://localhost:5000/transacoes/'

def obter_lista_clientes():
    response = requests.get(endpoint_clientes)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter a lista de clientes: {response.text}")
        return []

def criar_transacao_aleatoria(clientes):
    remetente = random.choice(clientes)
    recebedor = random.choice(clientes)
    
    while recebedor == remetente:
        recebedor = random.choice(clientes)
    
    valor = random.randint(1, 100)
    
    return {
        'remetente': remetente['id'],
        'recebedor': recebedor['id'],
        'valor': valor
    }

def enviar_transacao(transacao):
    response = requests.post(endpoint_transacoes + f"{transacao['remetente']}/{transacao['recebedor']}/{transacao['valor']}")
    if response.status_code == 200:
        print(f"Transação de {transacao['valor']} unidades de moeda de {transacao['remetente']} para {transacao['recebedor']} enviada com sucesso!")
    else:
        print(f"Erro ao enviar a transação: {response.text}")

def processar_transacoes(numero_de_transacoes, clientes):
    for _ in range(numero_de_transacoes):
        transacao = criar_transacao_aleatoria(clientes)
        enviar_transacao(transacao)

def main(numero_de_transacoes):
    clientes = obter_lista_clientes()
    if not clientes:
        print("Nenhum cliente encontrado. Encerrando o programa.")
        return
    
    processar_transacoes(numero_de_transacoes, clientes)

if __name__ == "__main__":
    numero_de_transacoes = 10
    main(numero_de_transacoes)