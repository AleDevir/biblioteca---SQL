'''
modelo Livro
'''
from src.model.livro import Livro
from src.model.exemplar import Exemplar

class LivroNaoRenovavel(Livro):
    '''
    classe Livro não renovável
    '''

    def renovar_emprestimo_exemplar(self, exemplar: Exemplar) -> None:
        '''
        Renova o empréstimo do exemplar após as validações.
        '''
        raise ValueError(f'\tNão é permitida renovação para este {exemplar}!')
