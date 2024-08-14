'''
pytest tests/test_color.py -vv
'''
from src.app_biblioteca import(
    limpar_console,
    verde,
    bright_amarelo,
    bright_vermelho,
    COR_BRANCA,
    COR_VERDE,
    COR_BRIGHT_AMARELA,
    COR_BRIGHT_VERMELHA
)

def test_limpar_console():
    '''
    Testa a exibição de menu.
    '''
    limpar_console()
    assert True

def test_conteudo_verde():
    '''
    Testa a função de colorir conteudo.
    '''
    text = 'texto'
    resposta = f"{COR_VERDE}{text}{COR_BRANCA}"
    coloracao_valida = verde(text)
    assert coloracao_valida == resposta

def test_conteudo_bright_amarelo():
    '''
    Testa a função de colorir conteudo.
    '''
    text = 'texto'
    resposta = f"{COR_BRIGHT_AMARELA}{text}{COR_BRANCA}"
    coloracao_valida = bright_amarelo(text)
    assert coloracao_valida == resposta

def test_conteudo_vermelho():
    '''
    Testa a função de colorir conteudo.
    '''
    text = 'texto'
    resposta = f"{COR_BRIGHT_VERMELHA}{text}{COR_BRANCA}"
    coloracao_valida = bright_vermelho(text)
    assert coloracao_valida == resposta
