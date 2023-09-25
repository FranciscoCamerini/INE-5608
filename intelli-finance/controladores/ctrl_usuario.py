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

    def login(self, cb = None):
        if dados := self.__tela.login_usuario():
            usuario = self.__banco.pega_usuario(dados["email"])
            if usuario: # Usuário existe
                if dados['senha'] == usuario["senha"]: #Login efetuado com sucesso
                    self.tela_principal()
                else:
                    self.__tela.popup("Senha incorreta")
                    self.login(cb)
            else: # Não existe usuário com este email
                self.__tela.popup("Não há cadastro com esse e-mail, por favor, tente novamente com outro e-mail ou cadastre esse.")
                self.login(cb)
        
        cb()
        

    def tela_principal(self):
        self.__tela.popup("LOGIN efetuado com sucesso")
        pass