'''
Data e hora 
'''
from datetime import datetime

def converter_timestamp_to_datetime(timestamp: float | int | str | datetime) -> datetime:
    '''
    Converte o TIMESTAMP em data e hora ex: 29/06/2024 09:26
    '''
    if isinstance(timestamp, datetime):
        return timestamp
    if isinstance(timestamp, str):
        return datetime.fromtimestamp(float(timestamp))
        #return converter_em_data_e_hora(timestamp)
    return datetime.fromtimestamp(timestamp)
