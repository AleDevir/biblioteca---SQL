'''
Módulo exemplar DB
Documentação de apoio: https://www.sqlitetutorial.net/
'''


from sqlite3 import Connection
from typing import Any

def drop_table_exemplares(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS exemplares")


def criar_tabela_exemplares(db_conection: Connection)-> None:
    '''
    Cria a tabela exemplares
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS exemplares(
                    id integer primary key autoincrement,
                    disponivel integer NOT NULL,                  
                    livro_id integer NOT NULL,
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE)''')

    db_conection.commit()


def insert_exemplar(
    db_conection: Connection,
    livro_id: int,
    disponivel: int = 1,
) -> int:
    '''
    Inseri exemplar na tabela.
    '''
    dados =  (
        disponivel,
        livro_id
    )

    db_conection.cursor().execute('INSERT INTO exemplares(disponivel, livro_id) VALUES(?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()


def tuple_to_dict(data: tuple) -> dict[str, int]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, livro_id, disponivel  =  data
    return {
        'id': identificacao,
        'disponivel': disponivel,
        'livro_id': livro_id,
    }

def get_exemplares_disponiveis(db_conection: Connection, disponivel: int = 1) -> dict[str, int]:
    '''
    Obter um exemplar disponivel.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, livro_id, disponivel FROM exemplares WHERE disponivel = {disponivel} ")
    exemplar_db = cursor.fetchall()
    result: list[dict[str, Any]] = []

    for data in exemplar_db:
        exemplar = tuple_to_dict(data)
        result.append(exemplar)
    return result


def get_exemplares_disponiveis_do_livro(db_conection: Connection, livro_id: int) -> dict[str, int]:
    '''
    Obter um exemplar disponivel.
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"SELECT id, livro_id, disponivel FROM exemplares WHERE livro_id = {livro_id} AND disponivel = 1 ")
    exemplar_db = cursor.fetchall()
    result: list[dict[str, Any]] = []

    for data in exemplar_db:
        exemplar = tuple_to_dict(data)
        result.append(exemplar)
    return result


def update_exemplar(
        db_conection: Connection,
        disponivel: int,
        identificacao: int,
    ) -> None:
    '''
    Atualiza dados do exemplar na tabela.
    '''
    db_conection.cursor().execute("UPDATE exemplares SET disponivel = ?  WHERE id = ?", (disponivel, identificacao)) # pylint: disable=line-too-long
    db_conection.commit()

##########################################################################
             # OUTRA INTERFACE DE RESPOSTA (PARA CONTAGEM) #
##########################################################################
def tuple_to_dict_count(data: tuple) -> dict[str, int]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}
    identificacao, livro_id, disponivel, qtd  =  data
    return {
        'id': identificacao,
        'disponivel': disponivel,
        'livro_id': livro_id,
        'qtd': qtd
    }


def quantidade_exemplares_disponiveis_by_livro_id(
        db_conection: Connection,
        id_livro: int
) -> list[dict[str, str]]:
    '''
    Obter exemplares do livro 
    '''
    cursor = db_conection.cursor()
    cursor.execute(f"""SELECT e.id, e.livro_id, e.disponivel, COUNT(*)
                        FROM exemplares AS e
                        WHERE  e.livro_id = {id_livro}
                        GROUP BY e.livro_id, e.disponivel
                    """)

    exemplares_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in exemplares_db:
        exemplar = tuple_to_dict_count(data)
        result.append(exemplar)
    return result


def contar_disponibilidade_do_livro(
    db_conection: Connection,
    livro_id: int,
    disponivel: int = 1,
) -> int:
    '''
    Obter quantidade de exemplares disponíveis do livro informado.
    '''
    quantidades = quantidade_exemplares_disponiveis_by_livro_id(db_conection, livro_id)

    if not quantidades:
        return 0

    quantidade = [e for e in quantidades if e['disponivel'] == disponivel]

    if not quantidade:
        return 0

    return quantidade[0]['qtd']


def quantidade_de_exemplares_disponiveis_do_livro(
    db_conection: Connection,
    livro_id: int
) -> int:
    '''
    Obter quantidade de exemplares disponíveis do livro informado.
    '''
    return contar_disponibilidade_do_livro(db_conection, livro_id)


def quantidade_de_exemplares_emprestados_do_livro(
    db_conection: Connection,
    livro_id: int
) -> int:
    '''
    Obter quantidade de exemplares disponíveis do livro informado.
    '''
    return contar_disponibilidade_do_livro(db_conection, livro_id, 0)
