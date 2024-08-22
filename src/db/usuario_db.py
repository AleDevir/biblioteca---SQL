'''
DB usuario
Documentação de apoio: https://www.sqlitetutorial.net/
'''
from typing import Any
from sqlite3 import Connection


def drop_table_usuarios(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS usuarios")


def criar_tabela_usuarios(db_conection: Connection)-> None:
    '''
    Cria a tabela usuarios
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS usuarios(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL,
                    telefone text UNIQUE NOT NULL,
                    nacionalidade text)''')

    db_conection.commit()


def insert_usuario(
    db_conection: Connection,
    nome: str,
    telefone: str,
    nacionalidade: str,
) -> None:
    '''
    Inseri usuario na tabela.
    '''
    dados = (nome, telefone, nacionalidade)
    db_conection.cursor().execute("INSERT INTO usuarios(nome, telefone, nacionalidade) VALUES(?, ?, ?)", dados)
    db_conection.commit()

def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, nome, telefone, nacionalidade =  data
    return {
        'id': identificacao,
        'nome': nome,
        'telefone': telefone,
        'nacionalidade': nacionalidade,
    }
def get_usuario_by_nome(db_conection: Connection, usuario_nome: str) -> dict[str, Any]:
    '''
    Obter um usuario pelo nome.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, nome, telefone, nacionalidade FROM usuarios WHERE nome = '{usuario_nome}' ")
    data = cursor.fetchone()
    return tuple_to_dict(data)