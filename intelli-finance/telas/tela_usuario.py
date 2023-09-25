import re

from telas.tela_base import Tela


class TelaUsuario(Tela):
    def __init__(self):
        super().__init__()

    def login_usuario(self):
        self.atualiza_tela(
            [
                [self.texto("Email:"), self.input("email")],
                [self.texto("Senha:"), self.input_senha("senha")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "confirmar":
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.login_usuario()

            return dados

    def cadastro_usuario(self) -> (dict, None):
        self.atualiza_tela(
            [
                [self.texto("Nome Completo:"), self.input("nome")],
                [self.texto("Email:"), self.input("email")],
                [self.texto("Sobre:")],
                [self.input_grande("sobre")],
                [self.texto("Senha:"), self.input_senha("senha1")],
                [self.texto("Confirmar Senha:"), self.input_senha("senha2")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "confirmar":
            if not re.match(r"^\S+@\S+\.\S+$", dados["email"]):
                self.popup("Entre um email válido!")

                return self.cadastro_usuario()

            if dados["senha1"] != dados["senha2"]:
                self.popup("As senhas não coincidem!")

                return self.cadastro_usuario()

            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.cadastro_usuario()
            return dados
