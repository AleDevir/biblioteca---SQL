'''
Data e hora 
'''
from datetime import datetime

def get_now() -> datetime:
    '''
    Retorna datetime now só com a data.
    '''
    agora = datetime.now()
    return datetime(agora.year, agora.month, agora.day, agora.hour, agora.minute, agora.second)
