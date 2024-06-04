from Controller.DBController import transactionsDB
from DBController import transactionsDB
import datetime

def Transaction(value:float, sender_id:str, sender_balance:float, time:datetime):
    # Se a resposta for 1, adiciona 
    pass

def is_rate_limited(user_id:str, time:datetime):
    db = transactionsDB()

    MAX_REQUESTS = 100
    TIME_WINDOW = 60
    current_time = time
    
    # Buscar registros de solicitações do usuário no TinyDB
    user_requests = db.get_user_requests(user_id)
    
    if user_requests:
        # Filtrar solicitações fora da janela de tempo
        recent_requests = db.filter_recent_requests(user_requests, current_time, TIME_WINDOW)
        if len(recent_requests) >= MAX_REQUESTS:
            return True
        else:
            # Atualizar registros no TinyDB
            db.update_user_requests(user_id, recent_requests, current_time)
            return False
    else:
        # Se não houver registros, adicionar o primeiro
        db.add_user_request(user_id, current_time)
        return False