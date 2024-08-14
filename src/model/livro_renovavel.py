'''
modelo Livro
'''

from src.model.livro import Livro
from src.model.exemplar import Exemplar

class LivroRenovavel(Livro):
    '''
    Classe livro renovável
    '''

    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''
        if not exemplar.pode_renovar(self.renovacoes_permitidas):
            raise ValueError(f'\tNão é possível renovar o empréstimo do livro {self.titulo}. Você já atingiu o limite máximo de renovações permitidas.') # pylint: disable=line-too-long

        exemplar.acrescentar_numero_renovacoes()
