from telas.tela_usuario import TelaUsuario
from bd.banco import Banco
from modelos.usuario import Usuario


class ControladorUsuario:
    def __init__(self):
        self.__tela = TelaUsuario()
        self.__banco = Banco()

    def realiza_cadastro(self, cb=None):
        if dados := self.__tela.cadastro_usuario():
            if self.__banco.pega_usuario(dados["email"]):
                self.__tela.popup("Este email já foi cadastrado!")

                return self.realiza_cadastro(cb)

            usuario = Usuario(
                dados["nome"], dados["email"], dados["sobre"], dados["senha1"]
            )
            self.__banco.inclui_usuario(usuario)
            self.__tela.popup("Usuário cadastrado com sucesso!")

        cb()

    def login(self):
        dados = self.__tela.login_usuario()
        usuario = self.__banco.pega_organizacao(dados['email'])
        if usuario is None:
            self.__tela.popup("Este E-mail não está registrado. Por favor, tente novamente com outro e-mail ou cadastre esse e-mail.")
        else:
            if usuario['senha'] == dados['senha']:
                self.tela_principal()
        

    def tela_principal(self):
        pass