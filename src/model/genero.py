'''
modelo Genero
'''
from typing import Self
from src.model.base import Base

class Genero(Base):
    '''
    classe Genero
    '''
    def __init__(
            self,
            nome: str,
            identificacao: int = 0
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome

    @classmethod
    def genero(
        cls,
        *,
        nome: str,
        identificacao: int,

        ) -> Self:
        '''
        Recebe os dados e retorna o  Genero)
        '''
        return cls(nome, identificacao)
