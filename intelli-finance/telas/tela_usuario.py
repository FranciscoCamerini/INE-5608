import re

from telas.tela_base import Tela


class TelaUsuario(Tela):
    def __init__(self):
        super().__init__()

    def principal(self, nome_usuario):
        self.atualiza_tela(
            [
                [self.titulo(f"Olá, {nome_usuario.capitalize()}!")],
                [self.botao("Organizações", chave="org")],
                [
                    self.botao(
                        "Editar Meu Perfil", chave="editar", pad=((0, 0), (10, 10))
                    )
                ],
                [self.botao("Deslogar", chave="logoff", pad=((0, 0), (20, 10)))],
            ],
            {"element_justification": "center"},
        )
        acao, dados = self.abrir()
        self.fechar()

        return acao, dados

    def organizacoes(self, organizacoes_p, organizacoes_a, organizacoes_f):
        elemento_orgs_p = []
        for org in organizacoes_p:
            elemento_orgs_p.append(
                [self.texto(org.nome), self.botao("Acessar", f"editar-{org.nome}")],
            )

        elemento_orgs_a = []
        for org in organizacoes_a:
            elemento_orgs_a.append(
                [self.texto(org.nome), self.botao("Acessar", f"editar-{org.nome}")],
            )

        elemento_orgs_f = []
        for org in organizacoes_f:
            elemento_orgs_p.append(
                [self.texto(org.nome), self.botao("Acessar", f"editar-{org.nome}")],
            )

        self.atualiza_tela(
            [
                [self.titulo("Suas Organizações:")],
                [self.texto("Proprietário:" if organizacoes_p else "")],
                elemento_orgs_p,
                [self.texto("Administrador:" if organizacoes_a else "")],
                elemento_orgs_a,
                [self.texto("Funcionário Restrito:" if organizacoes_f else "")],
                elemento_orgs_f,
                [
                    self.botao("Voltar", chave="voltar", pad=((0, 50), (70, 10))),
                    self.botao(
                        "Criar Organização", chave="criar_org", pad=((0, 50), (70, 10))
                    ),
                ],
            ],
            {"element_justification": "center"},
        )
        acao, dados = self.abrir()
        self.fechar()

        return acao, dados

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
                ]
                if not atualizacao
                else [],
                [self.texto("Sobre:")],
                [self.input_grande("sobre", valor=dados.get("sobre", ""))],
                *senhas,
                botoes,
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "confirmar":
            if not atualizacao and not re.match(r"^\S+@\S+\.\S+$", dados["email"]):
                self.popup("Entre um email válido!")

                return self.cadastro_usuario(dados, atualizacao)

            if not atualizacao and dados["senha1"] != dados["senha2"]:
                self.popup("As senhas não coincidem!")

                return self.cadastro_usuario(dados, atualizacao)

            if any(not dado for chave, dado in dados.items() if chave != "senha_nova"):
                self.popup("Favor preencher todos os campos!")

                return self.cadastro_usuario(dados, atualizacao)

        return acao, dados
