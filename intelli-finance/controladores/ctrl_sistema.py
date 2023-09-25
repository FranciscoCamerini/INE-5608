from telas.tela_inicial import TelaInicial

from .ctrl_usuario import ControladorUsuario


class ControladorSistema:
    def __init__(self):
        self.__tela = TelaInicial()
        self.__ctrl_usuario = ControladorUsuario()

    def cadastra_usuario(self):
        self.__ctrl_usuario.realiza_cadastro(cb=self.iniciar)

    def login(self):
        self.__ctrl_usuario.login(cb=self.iniciar)

    def iniciar(self):
        opcoes = {
            "cadastrar": self.cadastra_usuario,
            "logar": self.login,
        }

        opcao_escolhida = self.__tela.opcoes()
        if funcao := opcoes.get(opcao_escolhida):
            funcao()
