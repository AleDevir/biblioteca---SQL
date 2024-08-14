'''
Carga DB - criação de tabelas e inserção de dados.
'''

from datetime import datetime

from src.repositorio.repositorio_autor import(
    criar_tabela_autores,
    inserir_autor,
    drop_table_autores
)

from src.repositorio.repositorio_genero import(
    criar_tabela_generos,
    inserir_genero,
    drop_table_generos
)

from src.repositorio.repositorio_livro import(
    criar_tabela_livros,
    inserir_livro,
    drop_table_livros
)


from src.repositorio.repositoruio_emprestimo import(
    criar_tabela_emprestimos,
    inserir_emprestimo,
    drop_table_emprestimos
)

from src.repositorio.repositorio_usuario import(
    criar_tabela_usuarios,
    inserir_usuario,
    drop_table_usuarios
)



def carregar_banco_de_dados() -> None:
    '''
    Fluxo principal
    '''
    drop_table_autores()
    drop_table_generos()
    drop_table_livros()
    drop_table_emprestimos()
    drop_table_usuarios()


    criar_tabela_autores()
    criar_tabela_generos()
    criar_tabela_livros()
    criar_tabela_emprestimos()
    criar_tabela_usuarios() 


    #Autor
    inserir_autor('autor1')
    inserir_autor('autor1')
    inserir_autor('autor3')

    #Genero
    inserir_genero('Terror')
    inserir_genero('Romance')
    inserir_genero('Filosofia')

    # Livro
    inserir_livro()

    #Emprestimos
    agora = datetime.now()
    data_hora = datetime(agora.year, agora.month, agora.day)

    inserir_emprestimo()
  
    # Usuario
    inserir_usuario('Joana', 'Brasileira', '1111111111')
    inserir_usuario('Ana', 'Brasileira', '222222222')
    inserir_usuario('Maria', 'Brasileira', '333333333')
   
  
   