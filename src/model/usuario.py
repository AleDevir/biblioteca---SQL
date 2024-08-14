'''
modelo Usuario
'''

from typing import Self
from src.model.base import Base

class Usuario(Base):
    '''
    classe Usuario
    '''
    def __init__(
            self,
            nome: str,
            nacionalidade: str,
            telefone: str,
            identificacao: int
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.nome: str = nome
        self.nacionalidade: str = nacionalidade
        self.telefone: str = telefone

    @classmethod
    def usuario(
        cls,
        *,
        nome: str,
        nacionalidade: str,
        telefone: str,
        identificacao: int,

        ) -> Self:
        '''
        Recebe os dados e retorna o Usuario)
        '''
        return cls(nome, nacionalidade, telefone,  identificacao)
