import requests
import threading
import random
import time

# URL do endpoint Flask
endpoint_clientes = 'http://localhost:5000/cliente'
endpoint_transacoes = 'http://localhost:5000/transacoes/'

# Função para buscar a lista de clientes
def obter_lista_clientes():
    response = requests.get(endpoint_clientes)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter a lista de clientes: {response.text}")
        return []

# Função para criar uma transação aleatória entre dois clientes
def criar_transacao_aleatoria(clientes):
    remetente = random.choice(clientes)
    recebedor = random.choice(clientes)
    
    # Garante que remetente e recebedor são diferentes
    while recebedor == remetente:
        recebedor = random.choice(clientes)
    
    valor = random.randint(1, 100)
    
    return {
        'remetente': remetente['id'],
        'recebedor': recebedor['id'],
        'valor': valor
    }

# Função para enviar transação para o endpoint Flask
def enviar_transacao(transacao):
    response = requests.post(endpoint_transacoes + f"{transacao['remetente']}/{transacao['recebedor']}/{transacao['valor']}")
    if response.status_code == 200:
        print(f"Transação de {transacao['valor']} unidades de moeda de {transacao['remetente']} para {transacao['recebedor']} enviada com sucesso!")
    else:
        print(f"Erro ao enviar a transação: {response.text}")

# Função que cria e envia transações aleatórias
def processar_transacoes(numero_de_transacoes, clientes):
    for _ in range(numero_de_transacoes):
        transacao = criar_transacao_aleatoria(clientes)
        enviar_transacao(transacao)
        time.sleep(1)  # Espera um segundo entre cada transação

# Função principal que cria e envia transações aleatórias
def main(numero_de_transacoes):
    clientes = obter_lista_clientes()
    if not clientes:
        print("Nenhum cliente encontrado. Encerrando o programa.")
        return
    
    # Dividir o trabalho em threads
    threads = []
    for _ in range(numero_de_transacoes):
        t = threading.Thread(target=processar_transacoes, args=(1, clientes))
        threads.append(t)
        t.start()
    
    # Aguardar até que todas as threads terminem
    for t in threads:
        t.join()

if __name__ == "__main__":
    numero_de_transacoes = 1  # Número de transações a serem geradas
    main(numero_de_transacoes)