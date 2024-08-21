'''
DB usuario
Documentação de apoio: https://www.sqlitetutorial.net/
'''
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
