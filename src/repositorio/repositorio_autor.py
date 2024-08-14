'''
Repositório autor
'''

from sqlite3 import connect, Cursor
from src.model.autor import Autor

conexao_autor = connect('.\\src\\db\\banco_de_dados.db') # pylint: disable=line-too-long
cursor: Cursor = conexao_autor.cursor()


def drop_table_autores() -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    cursor.execute("DROP TABLE IF EXISTS autores")

#################################################
    # CRIAR & INSERIR AUTOR #
#################################################
def criar_tabela_autores()-> None:
    '''
    Cria a tabela autores
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS autores(
                    id integer primary key autoincrement,
                    nome varchar(100) NOT NULL)''')

    conexao_autor.commit()
    # conexao_autor.close()

def inserir_autor(nome: str) -> None:
    '''
    Inseri usuario na tabela.
    '''
    dados =  nome
    cursor.execute('INSERT INTO usuarios(nome) VALUES(?)', dados)
    conexao_autor.commit()

#################################################
    # INFRAESTRUTURA #
#################################################


def tuple_to_autor(data: tuple) -> Autor:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    identificacao, nome =  data
    return Autor.autor(
        identificacao=identificacao,
        nome=nome
    )



#################################################
    # GET - AUTOR #
#################################################

def get_autor_by_id(autor_id: int) -> Autor:
    '''
    Obter um autor pelo id.
    '''
    cursor.execute(f"SELECT * FROM autores WHERE id = {autor_id} ")
    data = cursor.fetchone()
    return tuple_to_autor(data)

def get_autor_by_nome(autor_nome: str) -> Autor:
    '''
    Obter um Autor pelo nome.
    '''
    cursor.execute(f"SELECT * FROM autores WHERE nome = '{autor_nome}' ")
    data = cursor.fetchone()
    return tuple_to_autor(data)

def get_autores() -> list[Autor]:
    '''
    Obter TODOS os autores
    '''
    cursor.execute('SELECT * FROM autores')
    autores_db = cursor.fetchall()
    result: list[Autor] = []
    for data in autores_db:
        autor = tuple_to_autor(data)
        result.append(autor)
    return result

#################################################
    # UPDATE - AUTOR #
#################################################

def update_autor(autor_nome: str,  autor_id: str) -> None:
    '''
    Atualiza dados do autor na tabela.
    '''
    cursor.execute("UPDATE autores SET nome = ?  WHERE id = ?", (autor_nome, autor_id)) # pylint: disable=line-too-long
    conexao_autor.commit()

#################################################
    # DELETE - AUTOR #
#################################################
def delete_autor(identificacao: int):
    '''
    Deleta um autor de id informado.
    '''
    cursor.execute("DELETE FROM autores WHERE id= ?", (str(identificacao)))
    conexao_autor.commit()
