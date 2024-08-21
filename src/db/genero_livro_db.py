'''
DB generos_livros
'''
from sqlite3 import Connection


def drop_table_generos_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já existir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS generos_livros")


def criar_tabela_generos_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela generos_livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS generos_livros(
                    genero_id integer NOT NULL,
                    livro_id interger NOT NULL,
                    PRIMARY KEY (livro_id, genero_id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY(genero_id) REFERENCES generos(id)
                        ON DELETE RESTRICT)''')

    db_conection.commit()


def insert_generos_livros(db_conection: Connection, genero_id: int, livro_id: int) -> None:
    '''
    Inseri genero_id e livro_id na tabela.
    '''
    dados = (genero_id, livro_id)
    db_conection.cursor().execute('INSERT INTO generos_livros(genero_id, livro_id) VALUES(?, ?)', dados)
    db_conection.commit()
