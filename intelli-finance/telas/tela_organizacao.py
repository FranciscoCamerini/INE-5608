import re

from telas.tela_base import Tela


class TelaOrganizacao(Tela):
    def __init__(self):
        super().__init__()

    def criar_organizacao(self) -> (dict, None):
        self.atualiza_tela(
            [
                [self.texto("Nome da Organização:"), self.input("nome")],
                [self.texto("Descrição:")],
                [self.input_grande("descrição")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Criar", "criar", pad=((85, 0), (35, 10))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "criar":
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.criar_organizacao()

            return dados

    def editar_organizacao(self, dados):
        self.atualiza_tela(
            [
                [
                    self.texto("Nome da Organização:"),
                    self.input_grande("nome", valor=dados.get("nome")),
                ],
                [self.texto("Descrição:")],
                [self.input_grande("descrição", valor=dados.get("descricao"))],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 20), (55, 0))),
                    self.botao("Usuários", "usuarios", pad=((0, 0), (55, 0))),
                    self.botao(
                        "Deletar Organização",
                        "deletar",
                        pad=((65, 25), (55, 0)),
                        cor="red",
                    ),
                    self.botao("Salvar", "salvar", pad=((55, 0), (55, 0))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "salvar":
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.editar_organizacao(dados)

        return acao, dados

    def listar_usuarios(self, dados):
        func_restritos = dados["funcionarios_restritos"]
        administradores = dados["administradores"]

        layout = []
        extra = {}
        if not (func_restritos or administradores):
            extra["size"] = (400, 200)
            layout.append(
                [self.texto("Sua organização ainda não possui outros membros.")]
            )

        if func_restritos:
            layout.append([self.titulo("Funcionários restritos:")])
            layout.append(
                [
                    [
                        [[self.texto(usuario.nome)], [self.texto(usuario.email)]],
                        self.botao("Editar", usuario.email, pad=((0, 0), (0, 40))),
                    ]
                    for usuario in func_restritos
                ]
            )

        if administradores:
            layout.append([self.titulo("Administradores:")])
            layout.append(
                [
                    [
                        [[self.texto(usuario.nome)], [self.texto(usuario.email)]],
                        self.botao("Editar", usuario.email),
                    ]
                    for usuario in administradores
                ]
            )

        layout.append(
            [
                [
                    self.botao("Voltar", "voltar", pad=((0, 200), (55, 0))),
                    self.botao("Adicionar Usuário", "add", pad=((0, 0), (55, 0))),
                ]
            ]
        )

        self.atualiza_tela(layout, extra)
        acao, _ = self.abrir()
        self.fechar()

        return acao

    def adicionar_usuario(self):
        self.atualiza_tela(
            [
                [self.texto("Email:")],
                [self.input("email")],
                [self.texto("Cargo:")],
                [
                    self.dropdown(
                        ["Administrador", "Funcionário Restrito"],
                        "Funcionário Restrito",
                    )
                ],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 30), (55, 0))),
                    self.botao("Confirmar", "confirmar", pad=((0, 0), (55, 0))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()

        if dados[0] == "Funcionário Restrito":
            dados["status"] = "funcionario_restrito"
        else:
            dados["status"] = "administrador"

        return acao, dados

    def edita_status_usuario(self, dados_usuario, status):
        self.atualiza_tela(
            [
                [self.texto(f"Nome: {dados_usuario['nome']}")],
                [self.texto(f"Email: {dados_usuario['email']}")],
                [self.texto(f"Sobre: {dados_usuario['sobre']}")],
                [self.texto("Cargo:")],
                [
                    self.dropdown(
                        ["Administrador", "Funcionário Restrito"],
                        "Funcionário Restrito"
                        if status == "funcionario_restrito"
                        else "Administrador",
                    )
                ],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 40), (55, 0))),
                    self.botao(
                        "Remover Usuário",
                        "remover",
                        pad=((0, 10), (55, 0)),
                        cor="red",
                    ),
                    self.botao("Confirmar", "confirmar", pad=((0, 0), (55, 0))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()

        if dados[0] == "Funcionário Restrito":
            dados["status"] = "funcionario_restrito"
        else:
            dados["status"] = "administrador"

        return acao, dados
