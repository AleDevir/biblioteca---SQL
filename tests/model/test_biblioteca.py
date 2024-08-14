# pylint: disable=line-too-long
'''
Testes da modelagem biblioteca.py
pytest tests/model/test_biblioteca.py -vv
'''
import os
from typing import Final
from datetime import datetime
import pytest
from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.livro_nao_renovavel import LivroNaoRenovavel
from src.model.livro_renovavel import LivroRenovavel
from src.model.emprestimo import Emprestimo, EMPRESTADO, DEVOLVIDO
from src.model.autor import Autor
from src.model.exemplar import Exemplar
from src.model.genero import Genero
from src.model.biblioteca import Biblioteca


USUARIO_1: Final[str] = Usuario('Alessandra', '222222222', 'brasileira', identificacao=1)
USUARIO_2: Final[str] = Usuario('Elanor', '222222222', 'neozelandes', identificacao=2)
USUARIO_3: Final[str] = Usuario('Amana', '333333333', 'brasileira', identificacao=3)

LIVRO_1: Final[str] = LivroRenovavel(
    titulo='Os irmãos Karamázov',
    editora='Martin Claret',
    generos=[Genero('Romance'), Genero('Suspense'), Genero('Ficção filosófica')],
    exemplares=[Exemplar(1), Exemplar(2), Exemplar(3)],
    autores=[Autor('Fiódor Dostoiévski')],
    renovacoes_permitidas=1,
    identificacao=1,
)
LIVRO_2: Final[str] = LivroNaoRenovavel(
    titulo='Crime e Castigo',
    editora='Martin Claret',
    generos=[Genero('Romance'), Genero('Suspense'), Genero('Ficção filosófica')],
    exemplares=[Exemplar(1)],
    autores=[Autor('Fiódor Dostoiévski')],
    identificacao=2,
)
LIVRO_3: Final[str] = LivroRenovavel(
    titulo='Zadig ou o Destinoo',
    editora='L&PM POCKET',
    generos=[Genero('Romance'), Genero('Suspense'), Genero('Ficção filosófica')],
    exemplares=[Exemplar(1)],
    autores=[Autor('Voltaire')],
    renovacoes_permitidas=3,
    identificacao=3,
)

# Habilita os caracteres ANSI escape no terminal Windows.
os.system("")

###########################################################
    # Cenários Empréstimos #
##########################################################
# @pytest.mark.skip(reason='desligado')
def test_emprestar():
    '''
    Teste de emprestimo
    pytest tests -vv
    '''
    usuario: Usuario = USUARIO_1
    livro: Livro = LIVRO_1
    biblioteca = Biblioteca([usuario], [livro])
    # identificacao_exemplar = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    emprestimo: Emprestimo = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    identificacao_exemplar = emprestimo.exemplar.identificacao

    # A identificaçao do exemplar emprestado deve ser um dos ids que constava nos exemplares do livro:
    assert identificacao_exemplar in [1,2,3]

    # O identificador não deve estar na lista de exemplares disponíveis para emprestar:
    assert identificacao_exemplar not in [e.identificacao for e in livro.exemplares]

    # O empréstimo deve constar no registro de emprestimos da Biblioteca:
    assert  len(biblioteca.emprestimos) == 1
    emprestimo: Emprestimo = biblioteca.emprestimos[0]
    assert emprestimo
    assert emprestimo.usuario == usuario
    assert emprestimo.livro == livro
    assert emprestimo.exemplar.identificacao == identificacao_exemplar
    assert emprestimo.estado == EMPRESTADO
    assert emprestimo.data_emprestimo <= datetime.now()
    assert emprestimo.data_devolucao is None

# @pytest.mark.skip(reason='desligado')
def test_emprestar_e_devolver():
    '''
    Teste de emprestimo
    pytest tests -vv
    '''
    usuario: Usuario = USUARIO_1
    livro: Livro = LIVRO_1
    biblioteca = Biblioteca([usuario], [livro])
    # identificacao_exemplar = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    emprestimo: Emprestimo = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    identificacao_exemplar = emprestimo.exemplar.identificacao



    # Asserções do realizar empréstimo não são necessárias, pois as mesmas já foram testadas em test_emprestar.
    biblioteca.devolver_emprestimo(emprestimo.identificacao)

    # O identificador deve VOLTAR para a lista de exemplares disponíveis para emprestar:
    assert identificacao_exemplar in [e.identificacao for e in livro.exemplares]

    # O empréstimo deve constar no registro de emprestimos da Biblioteca:
    assert  len(biblioteca.emprestimos) == 1
    emprestimo: Emprestimo = biblioteca.emprestimos[0]
    assert emprestimo
    assert emprestimo.usuario == usuario
    assert emprestimo.livro == livro
    assert emprestimo.exemplar.identificacao == identificacao_exemplar
    assert emprestimo.estado == DEVOLVIDO
    assert emprestimo.data_emprestimo <= datetime.now()
    assert emprestimo.data_devolucao <= datetime.now()


def test_emprestar_renovar_e_devolver():
    '''
    Teste de emprestimo
    pytest tests -vv
    '''
    usuario: Usuario = USUARIO_1
    livro: Livro = LIVRO_1
    biblioteca = Biblioteca([usuario], [livro])
    # identificacao_exemplar = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    emprestimo: Emprestimo = biblioteca.realizar_emprestimo(usuario.nome, livro.titulo)
    identificacao_exemplar = emprestimo.exemplar.identificacao

    # Asserções do realizar empréstimo não são necessárias, pois as mesmas já forma testadas em test_emprestar.

    biblioteca.renovar_emprestimo(emprestimo.identificacao)
    assert  len(biblioteca.emprestimos) == 1
    emprestimo: Emprestimo = biblioteca.emprestimos[0]
    assert emprestimo.exemplar.numero_de_renovacoes == 1

    try:
        biblioteca.renovar_emprestimo(emprestimo.identificacao)
        assert False
    except ValueError as erro:
        assert True
        assert str(erro) == '\tNão é possível renovar o empréstimo do livro Os irmãos Karamázov. Você já atingiu o limite máximo de renovações permitidas.'

    biblioteca.devolver_emprestimo(emprestimo.identificacao)

    # O identificador deve VOLTAR para a lista de exemplares disponíveis para emprestar:
    assert identificacao_exemplar in [e.identificacao for e in livro.exemplares]

    # O empréstimo deve constar no registro de emprestimos da Biblioteca:
    assert  len(biblioteca.emprestimos) == 1
    emprestimo: Emprestimo = biblioteca.emprestimos[0]
    assert emprestimo
    assert emprestimo.usuario == usuario
    assert emprestimo.livro == livro
    assert emprestimo.exemplar.identificacao == identificacao_exemplar
    assert emprestimo.estado == DEVOLVIDO
    assert emprestimo.data_emprestimo <= datetime.now()
    assert emprestimo.data_devolucao <= datetime.now()