import requests
import threading
import random
import string

url = 'http://localhost:5000/cliente'

def gerar_string_aleatoria(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def gerar_cliente_aleatorio():
    nome = gerar_string_aleatoria()
    senha = gerar_string_aleatoria(6)
    qtdMoedas = random.randint(0, 300)
    return {
        'nome': nome,
        'senha': senha,
        'qtdMoedas': float(qtdMoedas)
    }

def enviar_cliente():
    cliente = gerar_cliente_aleatorio()
    response = requests.post(f"{url}/{cliente['nome']}/{cliente['senha']}/{cliente['qtdMoedas']}")
    if response.status_code == 200:
        print(f"Cliente {cliente['nome']} enviado com sucesso!")
    else:
        print(f"Erro ao enviar o cliente {cliente['nome']}: {response.text}")

def main(numero_de_threads):
    threads = []
    for _ in range(numero_de_threads):
        thread = threading.Thread(target=enviar_cliente)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    numero_de_threads = 10
    main(numero_de_threads)
