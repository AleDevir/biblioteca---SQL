'''
DB genero
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection


def drop_table_generos(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS generos")


def criar_tabela_generos(db_conection: Connection)-> None:
    '''
    Cria a tabela generos
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS generos(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_genero(db_conection: Connection, nome: str) -> None:
    '''
    Inseri genero na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO generos(nome) VALUES(?)", (nome,))
    db_conection.commit()
