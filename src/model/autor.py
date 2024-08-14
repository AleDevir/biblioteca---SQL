'''
modelo Autor
'''
from typing import Self
from src.model.base import Base

class Autor(Base):
    '''
    classe Autor
    '''
    def __init__(
            self,
            nome: str,
            identificacao: int = 0,
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome

    @classmethod
    def autor(
        cls,
        *,
        nome: str,
        identificacao: int,

        ) -> Self:
        '''
        Recebe os dados e retorna o  Autor)
        '''
        return cls(nome, identificacao)
