'''
DB editora
Documentação de apoio: https://www.sqlitetutorial.net/
'''
from sqlite3 import Connection


def drop_table_editoras(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS editoras")


def criar_tabela_editoras(db_conection: Connection)-> None:
    '''
    Cria a tabela editoras
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS editoras(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_editora(db_conection: Connection, nome: str) -> None:
    '''
    Inseri editora na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO editoras(nome) VALUES(?)", (nome,))
    db_conection.commit()
