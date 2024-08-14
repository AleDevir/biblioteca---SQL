'''
modelo Base
'''

from abc import ABC

class Base(ABC):
    '''
    Clase base abstrata para o modelo.
    '''
    def __init__(self, identificacao: int = 0) -> None:
        '''
        Inicialização
        '''
        super().__init__()
        self._identificacao: int = identificacao

    @property
    def identificacao(self) -> int:
        '''
        Identificador
        O identificador com valor zero siginifica um novo objeto.
        '''
        return self._identificacao
