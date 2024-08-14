'''
modelo Emprestimo
'''
from typing import Self
from typing import Final
from datetime import datetime
from src.model.base import Base
from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.exemplar import Exemplar

EMPRESTADO: Final[str] = 'EMPRESTADO'
DEVOLVIDO: Final[str] = 'DEVOLVIDO'

class Emprestimo(Base):
    '''
    classe Emprestimo
    '''
    def __init__(
            self,
            usuario: Usuario,
            livro: Livro,
            exemplar: Exemplar,
            estado: str = EMPRESTADO,
            data_emprestimo: datetime = datetime.now(),
            data_devolucao: datetime | None = None,
            identificacao: int = 0,
    ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self.usuario: Usuario = usuario
        self.livro: Livro = livro
        self.exemplar: Exemplar = exemplar
        self.estado: str = estado
        self.data_emprestimo: datetime = data_emprestimo
        self.data_devolucao: datetime  | None = data_devolucao

    def devolver(self) -> None:
        '''
        Devolve um exemplar do livro emprestado na biblioteca
        '''
        if self.estado == DEVOLVIDO:
            raise ValueError(f'\tOperação não permitida! O {self.livro.titulo} já foi devolvido ao acervo da biblioteca.') # pylint: disable=line-too-long
        self.data_devolucao = datetime.now()
        self.estado = DEVOLVIDO
        self.livro.devolver_exemplar(self.exemplar.identificacao)

    def renovar(self) -> None:
        '''
        Renova o emprestimo do exemplar do livro emprestado pela biblioteca.
        '''
        if self.estado == DEVOLVIDO:
            raise ValueError(f'\tOperação não permitida! O {self.livro.titulo} já foi devolvido ao acervo da biblioteca.') # pylint: disable=line-too-long

        self.livro.renovar_emprestimo_exemplar(self.exemplar)

    @classmethod
    def emprestimo(
        # pylint: disable=too-many-arguments
        cls,
        *,
        usuario: Usuario,
        livro: Livro,
        exemplar: Exemplar,
        estado: str = EMPRESTADO,
        data_emprestimo: datetime = datetime.now(),
        data_devolucao: datetime | None = None,
        identificacao: int = 0,

        ) -> Self:
        '''
        Recebe os dados e retorna o  Exemplar)
        '''
        return cls(usuario, livro, exemplar, estado, data_emprestimo, data_devolucao, identificacao)
