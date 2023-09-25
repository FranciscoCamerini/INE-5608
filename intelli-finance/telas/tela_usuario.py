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

    def cadastro_usuario(self, dados: dict = None, atualizacao=False) -> (dict, None):
        dados = {} if not dados else dados

        botoes = [
            self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
            self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
        ]
        senhas = [
            [self.texto("Senha:"), self.input_senha("senha1")],
            [self.texto("Confirmar Senha:"), self.input_senha("senha2")],
        ]
        if atualizacao:
            botoes.insert(
                1, self.botao("Deletar", "deletar", pad=((85, 0), (35, 10)), cor="red")
            )
            senhas = [
                [self.texto("Senha Atual:"), self.input_senha("senha_atual")],
                [self.texto("Nova Senha (opcional):"), self.input_senha("senha_nova")],
            ]

        self.atualiza_tela(
            [
                [
                    self.texto("Nome Completo:"),
                    self.input("nome", valor=dados.get("nome", "")),
                ],
                [
                    self.texto("Email:"),
                    self.input("email", valor=dados.get("email", "")),
                ],
                [self.texto("Sobre:")],
                [self.input_grande("sobre", valor=dados.get("sobre", ""))],
                *senhas,
                botoes,
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "confirmar":
            if not re.match(r"^\S+@\S+\.\S+$", dados["email"]):
                self.popup("Entre um email válido!")

                return self.cadastro_usuario(dados, atualizacao)

            if not atualizacao and dados["senha1"] != dados["senha2"]:
                self.popup("As senhas não coincidem!")

                return self.cadastro_usuario(dados, atualizacao)

            if any(not dado for chave, dado in dados.items() if chave != "senha_nova"):
                self.popup("Favor preencher todos os campos!")

                return self.cadastro_usuario(dados, atualizacao)

        return acao, dados
