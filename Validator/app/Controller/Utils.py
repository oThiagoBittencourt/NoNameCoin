from datetime import datetime, timezone

current_server_time = datetime.now(timezone.utc)

def update_server_time(new_time):
    global current_server_time
    current_server_time = new_time

def get_current_server_time():
    return current_server_time