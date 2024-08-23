'''
Aplicação do gerenciamento da Biblioteca.
'''


from typing import Final, Any
from datetime import datetime, timedelta
import os
import platform
from sqlite3 import Connection, IntegrityError


from src.db.conexao_db import get_conexao_db
from src.db.carga_db import carregar_banco_de_dados

from src.db.livro_db import(
    get_livros_disponiveis_count,
    get_livros_emprestado_count,
    get_livros_by_autor_nome,
    get_livro_by_titulo,
    get_livro_by_id
)
from src.db.emprestimo_db import(
    get_emprestimos_atrasados,
    get_emprestimo_by_id,
    update_emprestimo_renovacao,
    update_emprestimo_devolucao,
    insert_emprestimo
)
from src.db.exemplar_db import(
    update_exemplar,
    quantidade_de_exemplares_disponiveis_do_livro,
    get_exemplares_disponiveis_do_livro
)
from src.db.autor_db import (
    delete_autor
)

from src.db.usuario_db import (
    get_usuario_by_nome,
)

COR_BRANCA: Final[str] = '\033[0;0m'
COR_BRIGHT_AMARELA: Final[str] = '\033[93m'
COR_VERDE: Final[str] = '\033[32m'
COR_BRIGHT_VERMELHA: Final[str] = '\033[91m'
LINHA_TRACEJADA: Final[str] = '-' * 81


OPCOES:  Final[dict[str, str ]] = {
    'C': 'Criação das Tabelas e  Inserção de Dados',
    '1': 'Listar todos os livros disponíveis',
    '2': 'Encontrar todos os livros emprestados no momento',
    '3': 'Localizar os livros escritos por um autor específico',
    '4': 'Verificar o número de cópias disponíveis de um determinado livro',
    '5': 'Mostrar os empréstimos em atraso',
    '6': 'Marcar um livro como devolvido',
    '7': 'Remover um autor',
    'E': 'Emprestar',
    'R': 'Renovar empréstimo',
    'D': 'devolver empréstimo',
    'S': 'Sair'    
}

OPCOES_SIM_NAO:  Final[dict[str, str ]] = {
    'S': 'Sim',    
    'N': 'Não',    
}



###########################################################
                  # INFRAESTRUTURA #
###########################################################

# Habilita os caracteres ANSI escape no terminal Windows.
os.system("")

def bright_amarelo(conteudo: Any) -> Any:
    '''
    Colore o texto informado em amarelo brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_AMARELA}{conteudo}{COR_BRANCA}"

def verde(conteudo: Any) -> Any:
    '''
    Colore o texto informado em verde.
    Retorna o texto colorido.
    '''
    return f"{COR_VERDE}{conteudo}{COR_BRANCA}"

def bright_vermelho(conteudo: Any) -> Any:
    '''
    Colore o texto informado em vermelho brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_VERMELHA}{conteudo}{COR_BRANCA}"

def limpar_console():
    '''
    Limpa o console de acordo com a plataforma.
    '''
    if platform.system() == 'Windows':
        os.system('cls')
    if platform.system() == 'Linux':
        os.system('clear')

def get_input(msg: str) -> str:
    '''
    Encapsula as chamadas dos inputs.
    Confecionda para poder testar os inputs.
    '''
    return input(msg)

def input_int(msg: str) -> int:
    '''
    Obtem número inteiro informado pelo usuário.
    Retorna o número.
    '''
    while True:
        try:
            return int(get_input(msg))
        except ValueError:
            print(bright_vermelho('\n\tApenas números inteiros são aceitos. Por favor, tente novamente.\n')) # pylint: disable=line-too-long

def input_opcoes(msg: str, opcoes: dict[str]) -> str:
    '''
    Obtem a opção válida.
    Retorna a opção.
    '''
    while True:
        opcao = get_input(msg).upper()
        if opcao in opcoes:
            return opcao
        print(f"\n\t'{bright_vermelho(opcao)}' opção inválida! As opções válidas são: {verde(', '.join(opcoes))}") # pylint: disable=line-too-long

def exibir_menu(opcoes: dict[str, str]) -> None:
    '''
    Exibi o menu de opções.
    '''
    print('')
    print(verde(f'\t{LINHA_TRACEJADA}'))
    print(verde('\tMENU DE OPÇÕES \n'))

    for key, value in opcoes.items():
        opcao = '|' + key + '|' + "  "  + value
        print(f"\t{verde(opcao)} ")
    print(verde(f'\t{LINHA_TRACEJADA}'))

def escolher_uma_opcao_do_menu_entrada(opcoes_menu_dict: dict[str, str]) -> str:
    '''
    Escolhe uma opção do menu.
    Retorna uma das opções do menu.
    '''
    exibir_menu(opcoes_menu_dict)
    siglas: list[str] = list(opcoes_menu_dict)
    escolher_opcao = input_opcoes('\n\tEntre com a opção desejada: ', siglas).upper() # pylint: disable=line-too-long
    while escolher_opcao not in siglas:
        escolher_opcao = input_opcoes(
            '\n\tEntre com a opção desejada: ',
             siglas
        ).upper()
    return escolher_opcao

def get_dado_str(msg_tipo_de_dado: str) -> str:
    '''
    obtem dado tipo str 
    Retorna o dado
    '''
    while True:
        tipo = get_input(f'\n\t{msg_tipo_de_dado}').lower()
        if tipo == '':
            print(bright_vermelho(f'\tValor inválido. O campo {tipo} deve ser preenchido.'))
        return tipo

def get_id(tipo_de_identificar: int) -> int:
    '''
    obtem o id.
    Retorna id
    '''
    while True:
        identificacao = input_int(f'\n\t{tipo_de_identificar}')
        if identificacao > 0:
            return identificacao
        print(bright_vermelho('\tValor  inválido. O identificador deve ser maior que zero.'))

######################################################
    # Exibir livros disponíveis ou emprestados #
######################################################

def exibir_disponibilidade_livros(msg, livros: list[dict[str, int]]) -> None:
    '''
    Exibe o resultado da opção escolhida
    '''

    print(bright_amarelo(f'\n\t{msg}'))
    print(bright_amarelo('\n\tTítulo & quantidade'))
    for livro in livros:
        titulo = livro['titulo']
        qtd = livro['qtd']
        print(bright_amarelo(f"\n\t{titulo} : {qtd}"))

####################################################################
    # Exibir quantidade de exemplares disponíveis de um livro #
####################################################################

def exibir_exemplares_do_livro(livro: dict[str, str], qtd: int = 0) -> None:
    '''
    Exibe os exemplares de um determinado livro.
    '''
    print(bright_amarelo(f'\n\tO livro de título {livro['titulo']}:'))
    print(bright_amarelo(f"\n\t Número de exemplares disponíveis: {qtd}"))

####################################################################
    # Exibir livros escritos por determinado autor #
####################################################################

def exibir_livro_escrito_por_autor( autor: str, livros: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''
    print(bright_amarelo(f'\n\tLivros escritos por {autor}:'))
    for livro in livros:
        titulo = livro['titulo']
        print(bright_amarelo(f"\n\t{titulo}"))

###########################################################
    # Exibir os emprestimos em atraso #
###########################################################

def exibir_emprestimos_em_atraso(emprestimos: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''
   
    print(bright_amarelo('\n\tEmpréstimos em atraso:'))
    for emprestimo in emprestimos:
        identificado_livro = emprestimo['livro_id']
        identificado_exemplar = emprestimo['exemplar_id']
        data_emprestimo = emprestimo['data_emprestimo']
        data_para_devolucao = emprestimo['data_para_devolucao']
        data_devolucao = emprestimo['data_devolucao']
        print(bright_amarelo(f"\n\tLivro de identificado: |{identificado_livro}|"))
        print(bright_amarelo(f"\n\tExemplar de identificado: |{identificado_exemplar}|"))
        print(bright_amarelo(f"\n\tData do empréstimo: {data_emprestimo}"))
        print(bright_amarelo(f"\n\tData para devolução: {data_para_devolucao}"))
        print(bright_amarelo(f"\n\tData de devolução: {data_devolucao}\n"))


###########################################################
    # Processos: EMPRESTAR | RENOVAR | DEVOLVER #
###########################################################

def emprestar(conexao: Connection) -> dict[str, Any]:
    '''
    Faz um emprestimo.
    '''

    nome = get_dado_str('\n\tNome do usúario: ')
    usuario = get_usuario_by_nome(conexao, nome)
    if not usuario:
        raise ValueError (bright_vermelho(f'O usuário {nome} não possui cadastro na biblioteca.'))

    titulo = get_dado_str('\n\tTítulo do livro: ')
    livro =  get_livro_by_titulo(conexao, titulo)
    if not livro:
        raise ValueError (bright_vermelho(f'O livro {titulo} não possui cadastro na biblioteca.'))

    exemplar = get_exemplares_disponiveis_do_livro(conexao, livro['id'])

    if not exemplar:
        raise ValueError (bright_vermelho(f'O livro {titulo} não possui exemplares disponíveis para empréstimo.'))

    exemplar_id = exemplar[0]['id']

    emprestimo_id = insert_emprestimo(
        db_conection = conexao,
        usuario_id = usuario['id'],
        livro_id = livro['id'],
        exemplar_id = exemplar_id,
    )
    update_exemplar(
        conexao,
        disponivel = 0,
        identificacao = exemplar_id,
    )
    return get_emprestimo_by_id(conexao, emprestimo_id)


def renovar_emprestimo(conexao: Connection, identificacao_emprestimo: int) -> dict[str, Any]:
    '''
    Renova o empréstimo.
    '''
    emprestimo = get_emprestimo_by_id(conexao, identificacao_emprestimo)
    if not emprestimo:
        raise ValueError (bright_vermelho(f'\n\tO empréstimo de identificação |{identificacao_emprestimo}| não existe na base de dados'))
    if emprestimo['estado'] == 'DEVOLVIDO':
        raise ValueError (bright_vermelho("\n\tEmpréstimo já foi devolvido."))
   
    livro = get_livro_by_id(conexao, emprestimo['livro_id'])
    renovacoes_permitidas = livro['renovacoes_permitidas']

    if renovacoes_permitidas <= 0:
        raise ValueError(bright_vermelho(f"\n\tO livro de título {livro['titulo']} não permite renovações."))

    numero_de_renovacoes = emprestimo['numero_de_renovacoes']

    if numero_de_renovacoes >= renovacoes_permitidas:
        raise ValueError(bright_vermelho(f"\n\tO livro de título {livro['titulo']} atingiu o limite de renovações permitidas: {renovacoes_permitidas}."))

    update_emprestimo_renovacao(
        conexao,
        identificacao= identificacao_emprestimo,
        numero_de_renovacoes = + 1,
        data_para_devolucao = datetime.now() + timedelta(days = 3),
    )
    update_exemplar(
        conexao,
        disponivel = 0,
        identificacao = emprestimo['exemplar_id'],
    )
    return get_emprestimo_by_id(conexao, identificacao_emprestimo)

def devolver_emprestimo(conexao: Connection, identificacao_emprestimo: int) -> dict[str, Any]:
    '''
    Devolve o empréstimo  de id 
    Retorna o Emprestimo como DEVOLVIDO.
    '''
    emprestimo = get_emprestimo_by_id(conexao, identificacao_emprestimo)
    if not emprestimo:
        raise ValueError (bright_vermelho(f'\n\tO empréstimo de identificação |{identificacao_emprestimo}| não existe na base de dados'))
    if emprestimo['estado'] == 'DEVOLVIDO':
        raise ValueError (bright_vermelho("\n\tEmpréstimo já foi devolvido."))

    update_emprestimo_devolucao(
        conexao,
        identificacao= identificacao_emprestimo,
        estado='DEVOLVIDO',
    )
    update_exemplar(
        conexao,
        disponivel = 1,
        identificacao = emprestimo['exemplar_id'],
    )
    return get_emprestimo_by_id(conexao, identificacao_emprestimo)


###########################################################
                  # CARREGAR BANCO DE DAODS #
###########################################################
def carregar_db(conexao: Connection) -> None:
    '''
    Fluxo da carga do banco de dados.
    '''
    try:
        while True:
            opcao = escolher_uma_opcao_do_menu_entrada(OPCOES_SIM_NAO)
            if opcao == 'S':
                carregar_banco_de_dados(conexao)
                print(bright_amarelo('\n\tCarga da base de dados realizada com sucesso!'))
                break
            if opcao == 'N':
                break
    except Exception as erro:
        print(bright_vermelho('\n\tNão foi possível realizar a carga da base de dados.'))
        print(bright_vermelho(f'\n\t{str(erro)}'))


###########################################################
                  # Biblioteca - DB #
###########################################################
def biblioteca_db() -> None:
    '''
    Fluxo Principal do Programa.
    '''
    try:
        conexao: Connection = get_conexao_db()
        limpar_console()
        print(verde('\t*** Biblioteca & Banco de Dados***\n '))
        while True:
            opcao = escolher_uma_opcao_do_menu_entrada(OPCOES)
            match opcao:
                case'C':
                    carregar_db(conexao)
                case '1':
                    livros = get_livros_disponiveis_count(conexao)
                    exibir_disponibilidade_livros('Livros disponíveis', livros)
                case'2':
                    livros = get_livros_emprestado_count(conexao)
                    exibir_disponibilidade_livros('Livros emprestados', livros)
                case'3':
                    nome = get_dado_str("Nome do autor: ")
                    livros = get_livros_by_autor_nome(conexao, nome)
                    if livros:
                        exibir_livro_escrito_por_autor(nome, livros)
                    else:
                        print(bright_vermelho(f'\n\t {nome} não possui livros associados.'))

                case'4':
                    titulo = get_dado_str("Título do livro: ")
                    livro =  get_livro_by_titulo(conexao, titulo)
                    if not livro:
                        print(bright_vermelho(f'\n\t {titulo} não encontrado na base de dados.'))
                    else:
                        quantidade = quantidade_de_exemplares_disponiveis_do_livro(conexao, livro['id'])
                        exibir_exemplares_do_livro(livro, quantidade)
                case '5':
                    emprestimo = get_emprestimos_atrasados(conexao)
                    exibir_emprestimos_em_atraso(emprestimo)
                case '6':
                    try:
                        identificacao = get_id("Identificação do empréstimo: ")
                        emprestimo = get_emprestimo_by_id(conexao, identificacao)
                        devolver_emprestimo(conexao, identificacao)
                        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{identificacao}| Devolvido com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                case '7':
                    try:
                        autor_id = get_id('\n\tIdentificação do autor: ')
                        delete_autor(conexao, autor_id)
                        print(bright_amarelo(f'\n\tAutor de identificação |{autor_id}| excluido com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                    except IntegrityError:
                        print(bright_vermelho(f"\n\tO autor de identificação |{autor_id}| não pode ser excluído porque possui livros associados."))
                case 'E':
                    try:                 
                        emprestimo_id = emprestar(conexao)
                        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{emprestimo_id}| realizado com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                
                case 'R':
                    try:
                        identificacao = get_id('\n\tIdentificação do empréstimo: ')
                        emprestimo = get_emprestimo_by_id(conexao, identificacao)
                        renovar_emprestimo(conexao, identificacao)
                        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{identificacao}| Renovado com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                case 'D':
                    try:
                        identificacao = get_id("Identificação do empréstimo: ")
                        emprestimo = get_emprestimo_by_id(conexao, identificacao)
                        devolver_emprestimo(conexao, identificacao)
                        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{identificacao}| Devolvido com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))

                case "S":
                    print(bright_amarelo('\n\tVocê saiu do sistema!'))
                    break
    except Exception as erro:
        print('ERRO!!!')
        print(bright_vermelho(erro))
        raise erro
    finally:
        conexao.close()
