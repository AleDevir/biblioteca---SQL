'''
Carga DB - criação de tabelas e inserção de dados.
'''
from datetime import timedelta
from sqlite3 import Connection

from src.util.data_hora_util import get_now

from src.db.autor_db import(
    criar_tabela_autores,
    insert_autor,
    drop_table_autores,
)
from src.db.genero_db import(
    criar_tabela_generos,
    insert_genero,
    drop_table_generos,
)
from src.db.editora_db import (
    criar_tabela_editoras,
    insert_editora,
    drop_table_editoras
)
from src.db.livro_db import(
    criar_tabela_livros,
    insert_livro,
    drop_table_livros
)
from src.db.autor_livro_db import(
    criar_tabela_autores_livros,
    insert_autores_livros,
    drop_table_autores_livros
)
from src.db.genero_livro_db import(
    criar_tabela_generos_livros,
    insert_generos_livros,
    drop_table_generos_livros
)
from src.db.exemplar_db import(
    criar_tabela_exemplares,
    insert_exemplar,
    drop_table_exemplares
)
from src.db.usuario_db import (
    criar_tabela_usuarios,
    insert_usuario,
    drop_table_usuarios,
)
from src.db.emprestimo_db import(
    criar_tabela_emprestimos,
    insert_emprestimo,
    drop_table_emprestimos
)


def carregar_banco_de_dados(db_conection: Connection) -> None:
    '''
    Fluxo principal
    '''
    drop_table_emprestimos(db_conection)
    drop_table_autores_livros(db_conection)
    drop_table_generos_livros(db_conection)
    drop_table_autores(db_conection)
    drop_table_generos(db_conection)
    drop_table_exemplares(db_conection)
    drop_table_livros(db_conection)
    drop_table_editoras(db_conection)
    drop_table_usuarios(db_conection)

    criar_tabela_usuarios(db_conection)
    criar_tabela_autores(db_conection)
    criar_tabela_generos(db_conection)
    criar_tabela_editoras(db_conection)
    criar_tabela_livros(db_conection)
    criar_tabela_autores_livros(db_conection)
    criar_tabela_generos_livros(db_conection)
    criar_tabela_exemplares(db_conection)
    criar_tabela_emprestimos(db_conection)

    # Usuario
    insert_usuario(db_conection, 'usuario1', '111101111', 'BRASIL')
    insert_usuario(db_conection, 'usuario2', '222202222', 'BRASIL')
    insert_usuario(db_conection, 'usuario3', '333303333', 'BRASIL')

    # Autor
    insert_autor(db_conection, 'autor1')
    insert_autor(db_conection, 'autor2')
    insert_autor(db_conection, 'autor3')
    # Autores que podem para excluidos, pois não possuem associação com livros.
    insert_autor(db_conection, 'autor4')
    insert_autor(db_conection, 'autor5')
    insert_autor(db_conection, 'autor6')


    # Genero
    insert_genero(db_conection, 'genero1')
    insert_genero(db_conection, 'genero2')
    insert_genero(db_conection, 'genero3')
    # Genero para excluir
    insert_genero(db_conection, 'genero4')
    insert_genero(db_conection, 'genero5')
    insert_genero(db_conection, 'genero6')


    # Editora
    insert_editora(db_conection, 'editora1')
    insert_editora(db_conection, 'editora2')
    insert_editora(db_conection, 'editora3')
    insert_editora(db_conection, 'editora4')

    # Livro
    insert_livro(db_conection, 'livro1', 0, 1)
    insert_livro(db_conection, 'livro2', 1, 2)
    insert_livro(db_conection, 'livro3', 2, 3)
    # Livro 4 adicionado para excluir autores_livros
    insert_livro(db_conection, 'livro4', 3, 4)

    # Exemplares do livro
    # Livro 1
    insert_exemplar(db_conection, 1, 0)
    # Livro 2
    insert_exemplar(db_conection, 2)
    insert_exemplar(db_conection, 2, 0)
    # Livro 3
    insert_exemplar(db_conection, 3, 0)
    insert_exemplar(db_conection, 3)
    insert_exemplar(db_conection, 3, 0)
    # Livro 4
    insert_exemplar(db_conection, 4)
    insert_exemplar(db_conection, 4)
    insert_exemplar(db_conection, 4)
    insert_exemplar(db_conection, 4)

    # Autores_Livros
    # Livro 1
    insert_autores_livros(db_conection, 1, 1)
    # Livro 2
    insert_autores_livros(db_conection, 1, 2)
    insert_autores_livros(db_conection, 2, 2)
    # Livro 3
    insert_autores_livros(db_conection, 1, 3)
    insert_autores_livros(db_conection, 2, 3)
    insert_autores_livros(db_conection, 3, 3)
    # Livro 4
    insert_autores_livros(db_conection, 1, 4)
    insert_autores_livros(db_conection, 2, 4)
    insert_autores_livros(db_conection, 3, 4)


    # Generos_Livros
    # Livro 1
    insert_generos_livros(db_conection, 1, 1)
    # Livro 2
    insert_generos_livros(db_conection, 1, 2)
    insert_generos_livros(db_conection, 2, 2)
    # Livro 3
    insert_generos_livros(db_conection, 1, 3)
    insert_generos_livros(db_conection, 2, 3)
    insert_generos_livros(db_conection, 3, 3)
    # Livro 4
    insert_generos_livros(db_conection, 1, 4)
    insert_generos_livros(db_conection, 2, 4)
    insert_generos_livros(db_conection, 3, 4)

    # Emprestimos
    hoje = get_now()
    ontem =  hoje + timedelta(days=-1) # ontem
    dois_dias_atras =  hoje + timedelta(days=-2) # Anteontem
    tres_dias_atras =  hoje + timedelta(days=-3) # 3 dias atrás
    quatro_dias_atras =  hoje + timedelta(days=-4) # 4 dias atrás

    amanha = hoje + timedelta(days=1) # amanhã
    depois_de_amanha = hoje + timedelta(days=2) # depois de amanhã
    daqui_a_tres_dias = hoje + timedelta(days=3) # daqui a três dias

    # Devolvidos
    insert_emprestimo(db_conection, 1, 1, 1, 'DEVOLVIDO', quatro_dias_atras, ontem, dois_dias_atras, 0)
    insert_emprestimo(db_conection, 1, 2, 2, 'DEVOLVIDO', tres_dias_atras, hoje, ontem, 1)
    insert_emprestimo(db_conection, 1, 3, 3, 'DEVOLVIDO', dois_dias_atras, amanha, hoje, 2)

    # Emprestado
    insert_emprestimo(db_conection, 1, 1, 1, 'EMPRESTADO', dois_dias_atras, amanha, None, 0)
    insert_emprestimo(db_conection, 1, 2, 2, 'EMPRESTADO', ontem, depois_de_amanha, None, 0)
    insert_emprestimo(db_conection, 1, 3, 3, 'EMPRESTADO', hoje, daqui_a_tres_dias, None, 0)

    # Atrasado
    insert_emprestimo(db_conection, 1, 3, 1, 'EMPRESTADO', quatro_dias_atras, ontem, None, 0)
    insert_emprestimo(db_conection, 2, 4, 2, 'EMPRESTADO', tres_dias_atras, hoje, None, 0)
