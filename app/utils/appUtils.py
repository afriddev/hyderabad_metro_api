from datetime import datetime
def get_current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M %p")