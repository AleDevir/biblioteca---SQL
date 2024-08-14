'''
Repositório genero
'''

from sqlite3 import connect, Cursor
from src.model.genero import Genero

conexao_genero = connect('.\\src\\db\\banco_de_dados.db') # pylint: disable=line-too-long
cursor: Cursor = conexao_genero.cursor()


def drop_table_generos() -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    cursor.execute("DROP TABLE IF EXISTS generos")

def criar_tabela_generos()-> None:
    '''
    Cria a tabela generos
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS generos(
                    id integer primary key autoincrement,
                    nome varchar(100) NOT NULL)''')

    conexao_genero.commit()
    # conexao_genero.close()


#################################################
    # INFRAESTRUTURA #
#################################################


def tuple_to_genero(data: tuple) -> Genero:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    identificacao, nome =  data
    return Genero.genero(
        identificacao=identificacao,
        nome=nome
    )


#################################################
    # INSERIR GENERO #
#################################################

def inserir_genero(nome: str) -> None:
    '''
    Inseri genero na tabela.
    '''
    dados =  nome
    cursor.execute('INSERT INTO generos(nome) VALUES(?)', dados)
    conexao_genero.commit()


#################################################
    # GET - GENERO #
#################################################

def get_genero_by_id(genero_id: int) -> Genero:
    '''
    Obter um genero pelo id.
    '''
    cursor.execute(f"SELECT * FROM generos WHERE id = {genero_id} ")
    data = cursor.fetchone()
    return tuple_to_genero(data)

def get_genero_by_nome(genero_nome: str) -> Genero:
    '''
    Obter um genero pelo nome.
    '''
    cursor.execute(f"SELECT * FROM generos WHERE nome = '{genero_nome}' ")
    data = cursor.fetchone()
    return tuple_to_genero(data)

def get_geneross() -> list[Genero]:
    '''
    Obter TODOS os generos
    '''
    cursor.execute('SELECT * FROM generos')
    genero_db = cursor.fetchall()
    result: list[Genero] = []
    for data in genero_db:
        genero = tuple_to_genero(data)
        result.append(genero)
    return result

#################################################
    # UPDATE - GENERO #
#################################################

def update_autor(genero_nome: str,  genero_id: str) -> None:
    '''
    Atualiza dados do genero na tabela.
    '''
    cursor.execute("UPDATE generos SET nome = ?  WHERE id = ?", (genero_nome, genero_id)) # pylint: disable=line-too-long
    conexao_genero.commit()

#################################################
    # DELETE - AUTOR #
#################################################
def delete_autor(identificacao: int):
    '''
    Deleta um autor de id informado.
    '''
    cursor.execute("DELETE FROM autores WHERE id= ?", (str(identificacao)))
    conexao_genero.commit()
