'''
Repositório autor
'''

from sqlite3 import connect, Cursor
from src.model.exemplar import Exemplar

conexao_exemplar = connect('.\\src\\db\\banco_de_dados.db') # pylint: disable=line-too-long
cursor: Cursor = conexao_exemplar.cursor()


def drop_table_exemplares() -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    cursor.execute("DROP TABLE IF EXISTS exemplares")

def criar_tabela_exemplares()-> None:
    '''
    Cria a tabela exemplares
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS exemplares(
                    id integer primary key autoincrement,
                    renovacoes integer NOT NULL)''')

    conexao_exemplar.commit()
    # conexao_exemplar.close()


#################################################
    # INFRAESTRUTURA #
#################################################


def tuple_to_exemplar(data: tuple) -> Exemplar:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    identificacao, renovacoes =  data
    return Exemplar.exemplar(
        identificacao=identificacao,
        numero_de_renovacoes=renovacoes
    )


#################################################
    # INSERIR EXEMPLAR #
#################################################

def inserir_exemplar(renovacoes: int) -> None:
    '''
    Inseri usuario na tabela.
    '''
    dados =  renovacoes
    cursor.execute('INSERT INTO exemplares(renovacoes) VALUES(?)', dados)
    conexao_exemplar.commit()


#################################################
    # GET - EXEMPLAR #
#################################################

def get_exemplar_by_id(renovacoes_id: int) -> Exemplar:
    '''
    Obter um aexemplar pelo id.
    '''
    cursor.execute(f"SELECT * FROM exemplares WHERE id = {renovacoes_id} ")
    data = cursor.fetchone()
    return tuple_to_exemplar(data)

def get_exemplares() -> list[Exemplar]:
    '''
    Obter TODOS os exemplarES
    '''
    cursor.execute('SELECT * FROM exemplares')
    exemplares_db = cursor.fetchall()
    result: list[Exemplar] = []
    for data in exemplares_db:
        exemplar = tuple_to_exemplar(data)
        result.append(exemplar)
    return result

#################################################
    # UPDATE - EXEMPLAR #
#################################################

def update_exemplar(renovacoes_quantidade: int, renovacoes_id: int) -> None:
    '''
    Atualiza dados do exemplar na tabela.
    '''
    cursor.execute("UPDATE exemplares SET renovacoes_quantidade = ?  WHERE id = ?", (renovacoes_quantidade, renovacoes_id)) # pylint: disable=line-too-long
    conexao_exemplar.commit()

#################################################
    # DELETE - EXEMPLAR #
#################################################
def delete_exemplar(identificacao: int):
    '''
    Deleta um exemplar de id informado.
    '''
    cursor.execute("DELETE FROM exemplares WHERE id= ?", (str(identificacao)))
    conexao_exemplar.commit()
