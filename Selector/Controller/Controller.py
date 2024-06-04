from Controller.DBController import transactionsDB
import datetime

def Transaction(value:float, sender_id:str, sender_balance:float, time:datetime):
    response = 1
    if (response == 1):
        transaction_register_controller(sender_id, time, UPDATE_MODE=True)

def is_rate_limited(sender_id:str, time:datetime):
    return transaction_register_controller(sender_id, time, UPDATE_MODE=False)

def transaction_register_controller(sender_id:str, time:datetime, UPDATE_MODE=False):
    db = transactionsDB()
    
    # Buscar registros de solicitações do usuário no TinyDB
    user_requests = db.get_user_requests(sender_id)
    
    if not UPDATE_MODE:
        TIME_WINDOW = 60
        MAX_REQUESTS = 100
        if user_requests:
            # Filtrar solicitações fora da janela de tempo
            recent_requests = db.filter_recent_requests(user_requests, time, TIME_WINDOW)
            if len(recent_requests) >= MAX_REQUESTS:
                return True
        return False
    if user_requests:
        db.update_user_requests(sender_id, recent_requests, time)
        return
    db.add_user_request(sender_id, time)
    return