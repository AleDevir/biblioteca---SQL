'''
Repositório usuario
'''

from sqlite3 import connect, Cursor
from src.model.usuario import Usuario

conexao_usuario = connect('.\\src\\db\\banco_de_dados.db') # pylint: disable=line-too-long
cursor: Cursor = conexao_usuario.cursor()


def drop_table_usuarios() -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    cursor.execute("DROP TABLE IF EXISTS usuarios")

def criar_tabela_usuarios()-> None:
    '''
    Cria a tabela usuarios
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios(
                    id integer primary key autoincrement,
                    nome varchar(100) UNIQUE NOT NULL,
                    nacionalidade varchar(100) NOT NULL,
                    telefone varchar(9) NOT NULL)''')

    conexao_usuario.commit()
    # conexao_usuario.close()



#################################################
    # INFRAESTRUTURA #
#################################################


def tuple_to_usuario(data: tuple) -> Usuario:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    identificacao, nome, nacionalidade, telefone =  data
    return Usuario.usuario(
        identificacao=identificacao,
        nome=nome,
        nacionalidade=nacionalidade,
        telefone=telefone
    )


#################################################
    # INSERIR USUARIO #
#################################################

def inserir_usuario(nome: str, nacionalidade: str, telefone: str) -> None:
    '''
    Inseri usuario na tabela.
    '''
    dados =  (nome, nacionalidade, telefone)
    cursor.execute('INSERT INTO usuarios(nome, nacionalidade, telefone) VALUES(?, ?, ?)', dados) # pylint: disable=line-too-long
    conexao_usuario.commit()


#################################################
    # GET - USUARIO #
#################################################

def get_usuario_by_id(usuario_id: int) -> Usuario:
    '''
    Obter um usuario pelo id.
    '''
    cursor.execute(f"SELECT * FROM usuarios WHERE id = {usuario_id} ")
    data = cursor.fetchone()
    return tuple_to_usuario(data)

def get_usuario_by_nome(usuario_nome: str) -> Usuario:
    '''
    Obter um Usuário pelo nome.
    '''
    cursor.execute(f"SELECT * FROM usuarios WHERE nome = '{usuario_nome}' ")
    data = cursor.fetchone()
    return tuple_to_usuario(data)

def get_usuario_by_nacionalidade(usuario_nacionalidade: str) -> Usuario:
    '''
    Obter um Usuário pela nacionalidade.
    '''
    cursor.execute(f"SELECT * FROM usuarios WHERE nacionalidade = '{usuario_nacionalidade}' ")
    data = cursor.fetchone()
    return tuple_to_usuario(data)

def get_usuario_by_telefone(usuario_telefone: str) -> Usuario:
    '''
    Obter um Usuário pelo telefone.
    '''
    cursor.execute(f"SELECT * FROM usuarios WHERE telefone = '{usuario_telefone}' ")
    data = cursor.fetchone()
    if not data:
        return None
    return tuple_to_usuario(data)

def get_usuarios() -> list[Usuario]:
    '''
    Obter TODOS os usuarios
    '''
    cursor.execute('SELECT * FROM usuarios')
    usuarios_db = cursor.fetchall()
    result: list[Usuario] = []
    for data in usuarios_db:
        usuario = tuple_to_usuario(data)
        result.append(usuario)
    return result

#################################################
    # UPDATE - USUARIO #
#################################################

def update_usuario(
        usuario_nome: str,
        usuario_nacionalidade: str,
        usuario_telefone: str,
        usuario_id: str
    ) -> None: 
    '''
    Atualiza dados do usuario na tabela.
    '''
    cursor.execute("UPDATE usuarios SET nome = ?, nacionalidade = ?, telefone = ? WHERE id = ?", (usuario_nome, usuario_nacionalidade, usuario_telefone, usuario_id)) # pylint: disable=line-too-long
    conexao_usuario.commit()

#################################################
    # DELETE - USUARIO #
#################################################
def delete_usuario(identificacao: int):
    '''
    Deleta um usuario de id informado.
    '''
    cursor.execute("DELETE FROM usuarios WHERE id= ?", (str(identificacao)))
    conexao_usuario.commit()
