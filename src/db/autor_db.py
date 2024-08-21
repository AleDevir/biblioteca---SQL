'''
DB autor
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection


def drop_table_autores(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS autores")


def criar_tabela_autores(db_conection: Connection)-> None:
    '''
    Cria a tabela autores
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS autores(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_autor(db_conection: Connection, nome: str) -> None:
    '''
    Inseri autor na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO autores(nome) VALUES(?)", (nome,))
    db_conection.commit()



def delete_autor(db_conection: Connection, identificacao: int):
    '''
    Deleta um autor de id informado.
    '''
    db_conection.cursor().execute("DELETE FROM autores WHERE id= ?", (str(identificacao)))
    db_conection.commit()
