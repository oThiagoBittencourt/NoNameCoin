import random
import string

def ramdom_port():
    return random.randint(0, 65535)

# Função para gerar uma string aleatória
def generate_random_string(size=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(size))

# Função para gerar um cliente aleatório
def create_validator():
    user = generate_random_string()
    password = generate_random_string(6)
    balance = random.randint(0, 300)
    return {
        'validator_user': user,
        'validator_password': password,
        'validator_balance': balance,
        'port' : None
    }