'''
Repositório emprestimo
'''

from sqlite3 import connect, Cursor
from datetime import datetime
from src.model.emprestimo import Emprestimo

conexao_emprestimo = connect('.\\src\\db\\banco_de_dados.db') # pylint: disable=line-too-long
cursor: Cursor = conexao_emprestimo.cursor()


def drop_table_emprestimos() -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    cursor.execute("DROP TABLE IF EXISTS emprestimos")

#################################################
    # CRIAR & INSERIR EMPRESTIMO #
#################################################

def criar_tabela_emprestimos()-> None:
    '''
    Cria a tabela emprestimos
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS emprestimos(
                    id integer primary key autoincrement,
                    usuario_id integer NOT NULL,
                    livro_id integer NOT NULL,
                    exemplar_id integer NOT NULL,
                    estado text NOT NULL,
                    data_emprestimo int NOT NULL,
                    data_devolucao int NOT NULL,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id),
                    FOREIGN KEY(exemplar_id) REFERENCES exemplares(id)
                   ''')


    conexao_emprestimo.commit()
    # conexao_emprestimo.close()

def inserir_emprestimo(
        usuario_id: int,
        livro_id: int,
        exemplar_id: int,
        estado: str,
        data_emprestimo: datetime,
        data_devolucao: datetime | None
        ) -> None:
    '''
    Inseri emprestimo na tabela.
    '''
    dados =  (
        usuario_id,
        livro_id,
        exemplar_id,
        estado,
        data_emprestimo,
        data_devolucao
    )
    cursor.execute('INSERT INTO emprestimos(usuario_id,livro_id, exemplar_id, estado, data_emprestimo, data_devolucao) VALUES(?, ?, ?, ?, ?, ?)', dados) # pylint: disable=line-too-long
    conexao_emprestimo.commit()


#################################################
    # INFRAESTRUTURA #
#################################################


def tuple_to_emprestimo(data: tuple) -> Emprestimo:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    usuario, livro, exemplar, estado, data_emprestimo, data_devolucao, identificacao =  data
    return Emprestimo.emprestimo(
       usuario=usuario,
       livro=livro,
       exemplar=exemplar,
       estado=estado,
       data_emprestimo=data_emprestimo,
       data_devolucao=data_devolucao,
       identificacao=identificacao
    )


#################################################
    # ADD - EMPRESTIMO #
#################################################

def add_emprestimo(
        emprestimo: Emprestimo
    ) -> None:
    '''
    Add Emprestimo
    '''
    # inserir_emprestimo(emprestimo.usuario, emprestimo.livro, )


#################################################
    # GET - EMPRESTIMO #
#################################################

def get_emprestimo_by_id(emprestimo_id: int) -> Emprestimo:
    '''
    Obter um emprestimo pelo id.
    '''
    cursor.execute(f"SELECT * FROM emprestimos WHERE id = {emprestimo_id} ")
    data = cursor.fetchone()
    return tuple_to_emprestimo(data)


def get_emprestimos() -> list[Emprestimo]:
    '''
    Obter TODOS os emprestimos
    '''
    cursor.execute('SELECT * FROM emprestimos')
    emprestimo_db = cursor.fetchall()
    result: list[Emprestimo] = []
    for data in emprestimo_db:
        emprestimo = tuple_to_emprestimo(data)
        result.append(emprestimo)
    return result

#################################################
    # UPDATE - EMPRESTIMO #
#################################################

def update_emprestimo(
        usuario_nome: str,
        livro_titulo: str,
        exemplar_id: int,
        data_emprestimo: datetime,
        data_devolucao: datetime | None,
        identificacao: int
    ) -> None:
    '''
    Atualiza dados do emprestimo na tabela.
    '''
    cursor.execute("UPDATE emprestimos SET usuario_nome = ?, livro_titulo = ?, data_emprestimo = ? data_devolucao = ? WHERE id = ?", (usuario_nome, livro_titulo, exemplar_id, data_emprestimo, data_devolucao, identificacao)) # pylint: disable=line-too-long
    conexao_emprestimo.commit()

#################################################
    # DELETE - EMPRESTIMO #
#################################################
def delete_emprestimo(identificacao: int):
    '''
    Deleta um emprestimo de id informado.
    '''
    cursor.execute("DELETE FROM emprestimos WHERE id= ?", (str(identificacao)))
    conexao_emprestimo.commit()
