from telas.tela_inicial import TelaInicial

from .ctrl_usuario import ControladorUsuario
from .ctrl_organizacao import ControladorOrganizacao


class ControladorSistema:
    def __init__(self):
        self.__tela = TelaInicial()
        self.__ctrl_usuario = ControladorUsuario()
        self.__ctrl_organizacao = ControladorOrganizacao()

    def cadastra_usuario(self):
        self.__ctrl_usuario.realiza_cadastro(cb=self.iniciar)

    def edita_usuario(self):
        self.__ctrl_usuario.edita_cadastro(usuario=None, cb=self.iniciar)

    def cria_organizacao(self):
        self.__ctrl_organizacao.cadastra_organizacao(cb=self.iniciar)

    def edita_organizacao(self):
        self.__ctrl_organizacao.edita_organizacao(cb=self.iniciar)

    def login(self):
        self.__ctrl_usuario.login(cb=self.iniciar)

    def iniciar(self):
        opcoes = {
            "cadastrar": self.cadastra_usuario,
            "editar": self.edita_usuario,
            "logar": self.login,
            "criar_org": self.cria_organizacao,
            "editar_org": self.edita_organizacao,
        }

        while True:
            opcao_escolhida = self.__tela.opcoes()
            if funcao := opcoes.get(opcao_escolhida):
                funcao()
            else:
                break
