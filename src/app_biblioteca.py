'''
Aplicação do gerenciamento da Biblioteca.
'''


from typing import Final, Any
from datetime import datetime
import os
import platform
from sqlite3 import Connection, IntegrityError


from src.db.conexao_db import get_conexao_db
from src.db.carga_db import carregar_banco_de_dados

from src.db.livro_db import(
    get_livros_disponiveis_count,
    get_livros_emprestado_count,
    get_livros_by_autor_nome,
    get_exemplares_by_titulo_livro
)
from src.db.emprestimo_db import(
    get_emprestimos_atrasados,
    get_emprestimo_by_id,
    update_emprestimo_devolucao
)
from src.db.exemplar_db import(
    update_exemplar
)
from src.db.autor_db import (
    delete_autor
)

COR_BRANCA: Final[str] = '\033[0;0m'
COR_BRIGHT_AMARELA: Final[str] = '\033[93m'
COR_VERDE: Final[str] = '\033[32m'
COR_BRIGHT_VERMELHA: Final[str] = '\033[91m'
LINHA_TRACEJADA: Final[str] = '-' * 31
LINHA_PONTILHADA: Final[str] = '-' * 41

OPCOES:  Final[dict[str, str ]] = {
    'C': 'Criação das Tabelas e  Inserção de Dados',
    '1': 'Listar todos os livros disponíveis',
    '2': 'Encontrar todos os livros emprestados no momento',
    '3': 'Localizar os livros escritos por um autor específico',
    '4': 'Verificar o número de cópias disponíveis de um determinado livro',
    '5': 'Mostrar os empréstimos em atraso',
    '6': 'Marcar um livro como devolvido',
    '7': 'Remover um autor',
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
    cabecalho = 'MENU DE OPÇÕES \n'
    print(verde(cabecalho.center(50)))

    for key, value in opcoes.items():
        opcao = '|' + key + '|' + "  "  + value
        print(f"\t\t{verde(opcao)} ")
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

def get_dado_str_(msg_tipo_de_dado: str) -> str:
    '''
    obtem dado tipo str 
    Retorna o dado
    '''
    while True:
        tipo = get_input(f'\n\t{msg_tipo_de_dado}').lower()
        if tipo == '':
            print(bright_vermelho(f'\tValor inválido. O campo {tipo} deve ser preenchido.'))
        return tipo

def get_id(tipo_de_dado: str) -> int:
    '''
    obtem o id.
    Retorna id
    '''
    while True:
        identificacao = input_int(f'\n\t{tipo_de_dado}')
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

    print(bright_amarelo(f'\n\t\t{msg}'))
    print(bright_amarelo(f'\t{LINHA_PONTILHADA}'))
    print(bright_amarelo('\n\tTítulo : quantidade'))
    for livro in livros:
        titulo = livro['titulo']
        qtd = livro['qtd']
        print(f"\n\t{titulo} : {qtd}")
    print(bright_amarelo(f'\t{LINHA_PONTILHADA}'))

####################################################################
    # Exibir quantidade de exemplares disponíveis de um livro #
####################################################################

def exibir_numero_exemplares_do_livro( titulo: str, livros: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''

    print(bright_amarelo(f'\n\t{LINHA_PONTILHADA}'))
    print(bright_amarelo(f'\n\t\t O livro de título {titulo}:'))
    for livro in livros:
        qtd_exemplares_disponiveis = livro['titulo']
        print(f"\n\t Número de exemplares disponíveis: {qtd_exemplares_disponiveis}")
    print(bright_amarelo(f'\t{LINHA_PONTILHADA}'))

####################################################################
    # Exibir livros escritos por determinado autor #
####################################################################

def exibir_livro_escrito_por_autor( autor: str, livros: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''

    print(bright_amarelo(f'\n\t{LINHA_PONTILHADA}'))
    print(bright_amarelo(f'\n\t\t Livros escritos por {autor}:'))
    for livro in livros:
        titulo = livro['titulo']
        print(f"\n\t Livro: {titulo}")
    print(bright_amarelo(f'\t{LINHA_PONTILHADA}'))

###########################################################
    # Exibir os emprestimos em atraso #
###########################################################

def exibir_emprestimos_em_atraso(emprestimos: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''

    print(bright_amarelo(f'\n\t{LINHA_PONTILHADA}'))
    print(bright_amarelo('\n\t\t Empréstimos em atraso:'))
    for emprestimo in emprestimos:
        identificado_livro = emprestimo['livro_id']
        data_emprestimo = emprestimo['data_emprestimo']
        data_para_devolucao = emprestimo['data_para_devolucao']
        data_devolucao = emprestimo['data_devolucao']
        print(f"\n\t\tLivro de identificado: |{identificado_livro}|")
        print(f"\n\t\tData do empréstimo: {data_emprestimo}")
        print(f"\n\t\tData para devolução: {data_para_devolucao}")
        print(f"\n\t\tData de devolução: {data_devolucao}\n")   
    print(bright_amarelo(f'\t{LINHA_PONTILHADA}'))

###########################################################
    # Processos: EMPRESTAR | RENOVAR | DEVOLVER #
###########################################################


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
        data_devolucao = datetime.now(),
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
                    nome = get_dado_str_("Nome do autor: ")
                    livros = get_livros_by_autor_nome(conexao, nome)
                    if livros:
                        exibir_livro_escrito_por_autor(nome, livros)
                    else:
                        print(bright_vermelho(f'\n\t {nome} não possui livros associados.'))
                case'4':
                    titulo = get_dado_str_("Título do livro: ")
                    livros = get_exemplares_by_titulo_livro(conexao, titulo)
                    if livros:            
                        exibir_numero_exemplares_do_livro(titulo, livros)
                    else:
                        print(bright_vermelho(f'\n\t {titulo} não encontrado.'))
                    print('\n\tDesenvolver ou inserir a funcionalidade: Verificar o número de cópias disponíveis de um determinado livro')
                case '5':
                    emprestimo = get_emprestimos_atrasados(conexao)
                    exibir_emprestimos_em_atraso(emprestimo)
                case '6':
                    try:
                        identificacao = get_id("empréstimo")
                        emprestimo = get_emprestimo_by_id(conexao, identificacao)
                        devolver_emprestimo(conexao, identificacao)
                        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{identificacao}| Devolvido com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                case '7':
                    try:
                        id_autor = get_id('\n\tIdentificação do autor: ')                          
                        delete_autor(conexao, id_autor)
                        print(bright_amarelo(f'\n\tAutor de identificação |{id_autor}| excluido com sucesso!'))
                    except ValueError as erro:
                        print(bright_vermelho(str(erro)))
                    except IntegrityError:
                        print(bright_vermelho(f"\n\tO autor de identificação |{id_autor}| não pode ser excluído porque possui livros associados."))
                case "S":
                    print(bright_amarelo('\n\tVocê saiu do sistema!'))
                    break
    except Exception as erro:
        print('ERRO!!!')
        print(bright_vermelho(erro))
        raise erro
    finally:
        conexao.close()
