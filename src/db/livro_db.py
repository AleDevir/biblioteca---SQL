'''
Módulo livro DB
Documentação de apoio:
    https://www.sqlitetutorial.net/ 
    https://www.sqlitetutorial.net/sqlite-count-function/
'''

from sqlite3 import Connection
from typing import Any


def drop_table_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS livros")


def criar_tabela_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS livros(
                    id integer primary key autoincrement,
                    titulo text NOT NULL,
                    renovacoes_permitidas integer NOT NULL,                  
                    editora_id integer NOT NULL,
                    FOREIGN KEY(editora_id) REFERENCES editoras(id)
                   )''')


    db_conection.commit()

def insert_livro(
    db_conection: Connection,
    titulo: str,
    renovacoes_permitidas: int,
    editora_id: int
) -> None:
    '''
    Inseri livro na tabela.
    '''
    dados =  (
        titulo,
        renovacoes_permitidas,
        editora_id
    )
    db_conection.cursor().execute('INSERT INTO livros(titulo, renovacoes_permitidas, editora_id) VALUES(?, ?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()

def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, titulo, renovacoes_permitidas,  editora_id  =  data
    return {
        'id': identificacao,
        'titulo': titulo,
        'renovacoes_permitidas': renovacoes_permitidas,
        'editora_id': editora_id,
    }

def get_livros_by_autor_nome(db_conection: Connection, autor_nome: str) -> list[dict[str, str]]:
    '''
    Obter todos os livros de um determinado autor
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"""SELECT l.id, l.titulo, l.renovacoes_permitidas, l.editora_id
                        FROM livros AS l
                        INNER JOIN  autores_livros AS al ON (l.id = al.livro_id)
                        INNER JOIN autores AS a ON (al.autor_id = a.id)
                        WHERE a.nome = '{autor_nome}' """)

    autores_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in autores_db:
        autor = tuple_to_dict(data)
        result.append(autor)
    return result

def get_livro_by_titulo(db_conection: Connection, titulo: str) -> dict[str, str]:
    '''
    Obter livro pelo titulo 
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"""SELECT l.id, l.titulo, l.renovacoes_permitidas, l.editora_id
                        FROM livros AS l
                        WHERE l.titulo = '{titulo}' """)

    livro_db = cursor.fetchone()
    return tuple_to_dict(livro_db)


##########################################################################
             # OUTRA INTERFACE DE RESPOSTA (PARA CONTAGEM) #
##########################################################################

def tuple_to_dict_count(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, titulo, renovacoes_permitidas,  editora_id, qtd  =  data
    return {
        'id': identificacao,
        'titulo': titulo,
        'renovacoes_permitidas': renovacoes_permitidas,
        'editora_id': editora_id,
        'qtd': qtd
    }

def get_livros_count(db_conection: Connection, disponivel: int) -> list[dict[str, int]]:
    '''
    Obter todos os livros disponíveis
    '''
    cursor = db_conection.cursor()

    cursor.execute(f"""SELECT l.id, l.titulo, l.renovacoes_permitidas, l.editora_id, COUNT(*)
                    FROM livros AS l
                    INNER JOIN exemplares AS e ON (e.livro_id = l.id)
                    WHERE e.disponivel = {disponivel}
                    GROUP BY l.id """)


    livros_disponiveis_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in livros_disponiveis_db:
        livro = tuple_to_dict_count(data)
        result.append(livro)
    return result

def get_livros_disponiveis_count(db_conection: Connection) -> list[dict[str, int]]:
    '''
    Obter todos os livros disponíveis
    '''
    return get_livros_count(db_conection, 1)

def get_livros_emprestado_count(db_conection: Connection) -> list[dict[str, int]]:
    '''
    Obter todos os livros disponíveis
    '''
    return get_livros_count(db_conection, 0)
