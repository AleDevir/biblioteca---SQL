'''
modelo Biblioteca
'''
from src.model.base import Base
from src.model.emprestimo import Emprestimo
from src.model.usuario import Usuario
from src.model.livro import Livro
from src.model.exemplar import Exemplar

class Biblioteca(Base):
    '''
    classe Biblioteca
    '''
    def __init__(
            self,
            usuarios: list[Usuario],
            livros: list[Livro],
            emprestimos: list[Emprestimo] = None,
            identificacao: int = 0,
        ) -> None:
        '''
        Inicialização
        '''
        super().__init__(identificacao)
        self._usuarios: list[Usuario] = usuarios
        self._livros: list[Livro] = livros
        self._emprestimos: list[Emprestimo] = []
        if emprestimos:
            self._emprestimos = emprestimos


    @property
    def usuarios(self) -> list[Usuario]:
        '''
        Lista de usuários        
        '''
        return self._usuarios

    @property
    def livros(self) -> list[Livro]:
        '''
        Lista de livros       
        '''
        return self._livros

    @property
    def emprestimos(self) -> list[Emprestimo]:
        '''
        Lista de empréstimos       
        '''
        return self._emprestimos

    def gerar_nova_identificacao_emprestimo(self) -> int:
        '''
        Gera uma identificacao para o emprestimo realizado.
        Retorna a identificacao.
        '''
        if not self.emprestimos:
            return 1
        valor_maximo_de_identificacao = max(e.identificacao for e in self.emprestimos)
        return valor_maximo_de_identificacao + 1

    def get_usuario_por_nome(self, nome_usuario: str) -> Usuario:
        '''
        Obtem o usuário por nome.
        Retorna o usuário.
        '''
        usuarios = [u for u in self.usuarios if u.nome.lower() == nome_usuario.lower()]
        if not usuarios:
            raise ValueError(f'\tO usuário |{nome_usuario}| não possui cadastro na Biblioteca.')

        return usuarios[0]

    def get_livro_por_titulo(self, titulo_livro: str) -> Livro:
        '''
        Obtem o livro por título.
        Retorna o livro.
        '''
        livros = [l for l in self.livros if l.titulo.lower() == titulo_livro.lower()]
        if not livros:
            raise ValueError(f'\tO livro |{titulo_livro}| não faz parte do acervo da Biblioteca.')

        return livros[0]

    def realizar_emprestimo(self, nome_usuario: str, titulo_livro: str) -> Emprestimo:
        '''
        Empresta ao usuario de nome o livro de título.
        Retorna o empréstimo.
        '''
        usuario: Usuario = self.get_usuario_por_nome(nome_usuario)
        livro: Livro = self.get_livro_por_titulo(titulo_livro)

        if not livro.possui_exemplar_disponivel:
            raise ValueError(f'\tO livro {livro.titulo} não possui exemplares disponíveis para empréstimo.') # pylint: disable=line-too-long

        exemplar: Exemplar = livro.retirar_exemplar()

        identificacao = self.gerar_nova_identificacao_emprestimo()
        emprestimo: Emprestimo = Emprestimo(
            usuario,
            livro,
            exemplar,
            identificacao=identificacao,
        )
        self.emprestimos.append(emprestimo)
        return emprestimo

    def get_emprestimo_realizado(
        self,
        identificacao_emprestimo: int
    ) -> Emprestimo:
        '''
        Obtem o emprestimo  realizado através da identificação. 
        Retorna o emprestimo.
        '''
        for emprestimo in self.emprestimos:
            if emprestimo.identificacao == identificacao_emprestimo:
                return emprestimo
        raise ValueError(f"\tO emprestimo de identificação |{identificacao_emprestimo}| não foi encontrado!") # pylint: disable=line-too-long

    def renovar_emprestimo(
            self,
            identificacao_emprestimo: int
    ) -> Emprestimo:
        '''
        Renova o emprestimo do livro (através da identificacao do empréstimo) 
        Retorna o emprestimo renovado.
        '''
        emprestimo = self.get_emprestimo_realizado(identificacao_emprestimo)
        emprestimo.renovar()
        return emprestimo

    def devolver_emprestimo(
            self,
            identificacao_emprestimo: int
    ) -> Emprestimo:
        '''
        Devolve a biblioteca o livro (identificação do empréstimo) de título 
        emprestado para o usuário de nome.
        Retorna o Emprestimo.
        '''
        emprestimo: Emprestimo = self.get_emprestimo_realizado(identificacao_emprestimo)
        emprestimo.devolver()
        return emprestimo
