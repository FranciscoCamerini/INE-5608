from datetime import datetime

from telas.tela_base import Tela


def valida_data(data_str):
    obj_data = None

    try:
        obj_data = datetime.strptime(data_str, "%d/%m/%Y")
    except Exception:
        pass

    try:
        obj_data = datetime.strptime(data_str, "%-d/%m/%Y")
    except Exception:
        pass

    return obj_data


class TelaOrganizacao(Tela):
    def __init__(self):
        super().__init__()

    def criar_organizacao(self) -> (dict, None):
        self.atualiza_tela(
            [
                [self.texto("Nome da Organização:"), self.input("nome")],
                [self.texto("Descrição:")],
                [self.input_grande("descricao")],
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

    def editar_organizacao(self, dados, status_usuario, notificacoes):
        pode_alterar_dados = status_usuario == "proprietario"

        botoes = [
            [
                self.botao("Voltar", "cancelar", pad=((0, 20), (55, 0))),
                self.botao("Usuários", "usuarios", pad=((0, 0), (55, 0))),
            ],
            [
                self.botao("Categorias", "categorias", pad=((0, 20), (55, 0))),
                self.botao("Registros", "registros", pad=((0, 0), (55, 0))),
            ],
        ]

        if status_usuario in ["proprietario", "administrador"]:
            botoes.append(
                self.botao(
                    "Notificações"
                    + (
                        f" ({len(notificacoes['despesas']) + len(notificacoes['receitas'])})"
                        if notificacoes
                        else ""
                    ),
                    "notificacoes",
                    pad=((0, 0), (55, 0)),
                )
            )
            botoes.append(self.botao("Logs", "log", pad=((20, 0), (55, 0))))
            botoes.append(self.botao("Relatório", "relatorio", pad=((20, 0), (55, 0))))

        if pode_alterar_dados:
            botoes.extend(
                [
                    self.botao(
                        "Deletar Organização",
                        "deletar",
                        pad=((65, 25), (55, 0)),
                        cor="red",
                    ),
                    self.botao("Salvar", "salvar", pad=((55, 0), (55, 0))),
                ]
            )

        self.atualiza_tela(
            [
                [
                    self.texto("Nome da Organização:"),
                    self.input_grande("nome", valor=dados.get("nome"))
                    if pode_alterar_dados
                    else self.texto(dados.get("nome")),
                ],
                [self.texto("Descrição:")],
                [
                    self.input_grande(
                        "descricao",
                        valor=dados.get("descricao"),
                    )
                    if pode_alterar_dados
                    else self.texto(dados.get("descricao"))
                ],
                botoes,
            ]
        )
        acao, dados = self.abrir()
        self.fechar()
        if acao == "salvar":
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.editar_organizacao(dados, status_usuario)

        return acao, dados

    def listar_categorias(self, dados: dict, status_usuario: str):
        # dados = {'nome': str, categoria: 'Receita' || 'Despesa', 'descricao': str}
        categorias = dados["categorias"]
        editor = status_usuario == "administrador" or status_usuario == "proprietario"
        layout = []
        extra = {}
        if not categorias:
            extra["size"] = (400, 200)
            layout.append(
                [
                    self.texto(
                        "Sua organização não possui categorias de transação.",
                        size=(140, 1),
                    )
                ]
            )
        else:
            layout.append([self.titulo("Categorias de transação")])
            for categ in categorias:
                sub_layout = [
                    [[self.texto(f"{categ.nome} -> {categ.tipo}", size=(60, 1))]]
                ]
                layout.append(sub_layout)
        botoes = [
            self.botao("Voltar", "voltar", pad=((0, 50), (55, 0))),
        ]
        if editor:
            botoes.append(
                self.botao("Adicionar Categoria", "add", pad=((0, 0), (55, 0)))
            )

        layout.append([botoes])

        self.atualiza_tela(layout, extra)
        acao, _ = self.abrir()
        self.fechar()

        return acao

    def adicionar_categoria(self):
        self.atualiza_tela(
            [
                [self.texto("Nome:")],
                [self.input("nome")],
                [self.texto("Categoria:")],
                [
                    self.dropdown(
                        ["Receita", "Despesa"],
                        "Receita",
                    )
                ],
                [self.texto("Descrição")],
                [self.input_grande("descricao")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 30), (55, 0))),
                    self.botao("Confirmar", "confirmar", pad=((0, 0), (55, 0))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()

        if dados[0] == "Receita":
            dados["categoria"] = "Receita"
        else:
            dados["categoria"] = "Despesa"
        # dados = {'nome': str, categoria: 'Receita' || 'Despesa', 'descricao': str}
        if any(not dado for dado in dados.values()):
            self.popup("Favor preencher todos os campos!")

            return self.adicionar_categoria()

        return acao, dados

    def listar_usuarios(self, dados, status_usuario):
        proprietario = dados["proprietario"]
        func_restritos = dados["funcionarios_restritos"]
        administradores = dados["administradores"]

        eh_proprietario = status_usuario == "proprietario"

        layout = [
            [self.titulo("Proprietário:")],
            [[self.texto(proprietario.nome)], [self.texto(proprietario.email)]],
        ]
        if not (func_restritos or administradores):
            layout.append(
                [self.texto("Sua organização ainda não possui outros membros.")]
            )

        if func_restritos:
            layout.append([self.titulo("Funcionários restritos:")])
            for usuario in func_restritos:
                sub_layout = [
                    [[self.texto(usuario.nome)], [self.texto(usuario.email)]],
                ]
                if eh_proprietario:
                    sub_layout.append(
                        self.botao("Editar", usuario.email, pad=((0, 0), (0, 40)))
                    )
                layout.append(sub_layout)

        if administradores:
            layout.append([self.titulo("Administradores:")])
            for usuario in administradores:
                sub_layout = [
                    [[self.texto(usuario.nome)], [self.texto(usuario.email)]],
                ]
                if eh_proprietario:
                    sub_layout.append(
                        self.botao("Editar", usuario.email, pad=((0, 0), (0, 40)))
                    )
                layout.append(sub_layout)

        botoes = [
            self.botao("Voltar", "voltar", pad=((0, 20), (55, 0))),
        ]
        if eh_proprietario:
            botoes.append(self.botao("Adicionar Usuário", "add", pad=((0, 0), (55, 0))))

        layout.append([botoes])

        self.atualiza_tela(layout)
        acao, _ = self.abrir()
        self.fechar()

        return acao

    def pega_dados_adicionar_usuario(self):
        self.atualiza_tela(
            [
                [self.texto("Email do Usuário:")],
                [self.input("email")],
                [self.texto("Tipo do Usuário:")],
                [
                    self.dropdown(
                        ["Administrador", "Funcionário Restrito"],
                        "Funcionário Restrito",
                    )
                ],
                [self.texto("Confirme sua senha:")],
                [self.input_senha("senha")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 30), (55, 0))),
                    self.botao("Adicionar", "confirmar", pad=((0, 0), (55, 0))),
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
                [self.texto("Tipo do Usuário:")],
                [
                    self.dropdown(
                        ["Administrador", "Funcionário Restrito"],
                        "Funcionário Restrito"
                        if status == "funcionario_restrito"
                        else "Administrador",
                    )
                ],
                [self.texto("Confirme sua senha:")],
                [self.input_senha("senha")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 40), (55, 0))),
                    self.botao(
                        "Remover Usuário",
                        "remover",
                        pad=((0, 10), (55, 0)),
                        cor="red",
                    ),
                    self.botao("Salvar", "confirmar", pad=((0, 0), (55, 0))),
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

    def listar_registros_financeiros(self, status_usuario: str, dados: dict):
        despesas = dados["despesas"]
        receitas = dados["receitas"]
        layout = []

        layout.append([self.titulo("Despesas:")])
        if not despesas:
            layout.append(
                [
                    self.texto(
                        "Sua organização não possui nenhuma despesa.", size=(100, 1)
                    )
                ]
            )
        else:
            for i, despesa in enumerate(despesas):
                sub_layout = [
                    self.texto(
                        f"{despesa.valor} -> {despesa.categoria}, Data: {despesa.data}",
                        size=(120, 1),
                    )
                ]
                if (
                    status_usuario == "proprietario"
                    or despesa.status_autor == "funcionario_restrito"
                    and status_usuario == "administrador"
                ):
                    sub_layout.append(self.botao("Editar", f"editar_despesa:{i}"))

                layout.append(sub_layout)

        layout.append([self.titulo("Receitas:")])
        if not receitas:
            layout.append(
                [
                    self.texto(
                        "Sua organização não possui nenhuma receita.", size=(100, 1)
                    )
                ]
            )
        else:
            for i, receita in enumerate(receitas):
                sub_layout = [
                    self.texto(
                        f"{receita.valor} -> {receita.categoria}, Data: {receita.data}",
                        size=(120, 1),
                    )
                ]
                if (
                    status_usuario == "proprietario"
                    or receita.status_autor == "funcionario_restrito"
                    and status_usuario == "administrador"
                ):
                    sub_layout.append(self.botao("Editar", f"editar_receita:{i}"))

                layout.append(sub_layout)

        botoes = [
            self.botao("Voltar", "voltar", pad=((0, 50), (55, 0))),
            self.botao("Adicionar Despesa", "addDespesa", pad=((0, 0), (55, 0))),
            self.botao("Adicionar Receita", "addReceita", pad=((0, 0), (55, 0))),
        ]

        layout.append([botoes])

        self.atualiza_tela(layout)
        acao, _ = self.abrir()
        self.fechar()

        return acao

    def adicionar_registro_financeiro(self, categorias_org, tipo, dados_input={}):
        categorias = []

        if tipo == "receita":
            for cat in categorias_org:
                if cat.tipo == "Receita":
                    categorias.append(cat.nome)

        else:
            for cat in categorias_org:
                if cat.tipo == "Despesa":
                    categorias.append(cat.nome)

        def validar_valor(valor: str) -> bool:
            """Valida se o valor é um número."""
            try:
                float(valor)
            except Exception:
                return False
            else:
                return True

        botoes = [
            self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
            self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
        ]
        if dados_input:
            botoes.insert(
                1,
                self.botao("Deletar", "deletar", pad=((85, 0), (35, 10)), cor="red"),
            )

        self.atualiza_tela(
            [
                [self.texto("Tipo:")],
                [
                    self.radio(
                        "Receita",
                        "RADIO1",
                        default=(tipo == "receita"),
                        key="Receita",
                        disabled=True,
                    ),
                    self.radio(
                        "Despesa",
                        "RADIO1",
                        default=(tipo == "despesa"),
                        key="Despesa",
                        disabled=True,
                    ),
                ],
                [
                    self.texto("Categoria:"),
                    self.combo(
                        categorias,
                        valor_default=categorias[0]
                        if not dados_input
                        else dados_input["categoria"],
                        tamanho=(20, 1),
                        chave="categoria",
                        readonly=True,
                    ),
                ],
                [
                    self.texto("Valor:"),
                    self.input(
                        "valor", valor="" if not dados_input else dados_input["valor"]
                    ),
                ],
                [self.texto("Descrição:")],
                [
                    self.multiline(
                        "" if not dados_input else dados_input["descricao"],
                        tamanho=(25, 3),
                        chave="descricao",
                    )
                ],
                [
                    self.texto("Data:"),
                    self.input("data", "" if not dados_input else dados_input["data"]),
                ],
                botoes,
            ]
        )
        acao, dados = self.abrir()
        self.fechar()

        # Determina o tipo e depois exclui as chaves indesejadas
        if dados.get("Receita"):
            dados["tipo"] = "Receita"
        else:
            dados["tipo"] = "Despesa"
        del dados["Receita"]
        del dados["Despesa"]

        if acao == "confirmar":
            # Verifica se existem dados faltando
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")
                return self.adicionar_registro_financeiro(categorias_org, tipo)

            # Verifica a validade do valor
            if not validar_valor(dados["valor"]):
                self.popup("O valor deve conter somente números.")
                return self.adicionar_registro_financeiro(categorias_org, tipo)

            # Verifica a validade da data
            if not valida_data(dados["data"]):
                self.popup("A data deve estar no formato dd/mm/aaaa.")
                return self.adicionar_registro_financeiro(categorias_org, tipo)

        return acao, dados

    def listar_notificacoes(self, notificacoes):
        layout = []

        if notificacoes.get("despesas"):
            layout.append([self.titulo("Despesas Dos Próximos 7 Dias")])

            for registro in notificacoes["despesas"]:
                layout.append(
                    [
                        self.texto(
                            f"{registro.data} -> Categoria: {registro.categoria}. Valor: {registro.valor}",
                            size=(100, 1),
                        )
                    ]
                )

        if notificacoes.get("receitas"):
            layout.append([self.titulo("Receitas Dos Próximos 7 Dias")])

            for registro in notificacoes["receitas"]:
                layout.append(
                    [
                        self.texto(
                            f"{registro.data} -> Categoria: {registro.categoria}. Valor: {registro.valor}",
                            size=(100, 1),
                        )
                    ]
                )

        if not (notificacoes.get("despesas") or notificacoes.get("receitas")):
            layout.append(self.titulo("Não há notificações"))

        self.atualiza_tela(
            [layout, [self.botao("Voltar", "voltar", pad=((0, 0), (30, 0)))]]
        )

        self.abrir()
        self.fechar()

    def pega_dados_relatorio(
        self, relatorios, categorias_receita, categorias_despesa, listar=True
    ):
        acao = ""
        if listar:
            layout_relatorios = []
            for relatorio in relatorios:
                layout_relatorios.append(
                    [
                        self.texto(relatorio.nome),
                        self.botao("Exportar", f"exportar:{relatorio.nome}"),
                        self.botao(
                            "Detalhes",
                            f"detalhes:{relatorio.nome}",
                            pad=((20, 0), (0, 0)),
                        ),
                    ]
                )

            self.atualiza_tela(
                [
                    [self.titulo("Relatórios")],
                    layout_relatorios,
                    [
                        self.botao("Voltar", "voltar", pad=((0, 0), (60, 0))),
                        self.botao("Novo Relatório", "novo", pad=((100, 0), (60, 0))),
                    ],
                ]
            )

            acao, dados = self.abrir()
            self.fechar()

        if not listar or acao == "novo":
            self.atualiza_tela(
                [
                    [self.texto("Nome Relatório: "), self.input("nome")],
                    [self.texto("Data Início: "), self.input("data_inicio")],
                    [self.texto("Data Fim: "), self.input("data_fim")],
                    [self.texto("Formato datas: DD/MM/AAAA", font_size=12)],
                    [self.texto("Categorias Incluídas (Receitas)")],
                    [self.lista(categorias_receita, chave="categorias_receita")],
                    [self.texto("Categorias Incluídas (Despesas)", size=(28, 1))],
                    [self.lista(categorias_despesa, chave="categorias_despesa")],
                    [self.texto("Confirme sua senha: "), self.input_senha("senha")],
                    [
                        self.botao("Cancelar", "cancelar"),
                        self.botao("Gerar", "gerar", pad=((100, 0), (0, 0))),
                    ],
                ]
            )

            acao, dados = self.abrir()
            self.fechar()

        if acao == "gerar":
            if not dados["nome"]:
                self.popup("O campo 'nome' é obrigatório!")
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )

            data_inicio = valida_data(dados["data_inicio"])
            data_fim = valida_data(dados["data_fim"])

            if not data_inicio:
                self.popup("Data de início inválida! Formato esperado: DD/MM/AAAA")
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )

            if not data_fim:
                self.popup("Data de fim inválida! Formato esperado: DD/MM/AAAA")
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )

            if not data_fim > data_inicio:
                self.popup("A data final deve ser maior do que a data inicial!")
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )

            if not dados["senha"]:
                self.popup("O campo 'senha' é obrigatório")
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )

            if acao == "cancelar":
                return self.pega_dados_relatorio(
                    relatorios, categorias_receita, categorias_despesa, listar=False
                )
        elif acao == "cancelar":
            return self.pega_dados_relatorio(
                relatorios, categorias_receita, categorias_despesa
            )

        return acao, dados

    def mostra_dados_relatorio(self, relatorio):
        layout = [
            [self.titulo(relatorio.nome)],
            [self.texto("Autor: ", estilo="bold"), self.texto(relatorio.autor.nome)],
            [
                self.texto("Data Início: ", estilo="bold"),
                self.texto(relatorio.data_inicio),
            ],
            [self.texto("Data Fim: ", estilo="bold"), self.texto(relatorio.data_fim)],
        ]

        if relatorio.categorias_receita:
            sublayout = [[self.texto("Categorias Receita: ", estilo="bold")]]
            sublayout.append(
                [self.texto(f"- {cat}") for cat in relatorio.categorias_receita]
            )
            layout.append(sublayout)

        if relatorio.categorias_despesa:
            sublayout = [[self.texto("Categorias Despesa: ", estilo="bold")]]
            sublayout.append(
                [self.texto(f"- {cat}") for cat in relatorio.categorias_despesa]
            )
            layout.append(sublayout)

        layout.append(
            [
                self.botao("Voltar", "voltar", pad=((70, 0), (20, 0))),
                self.botao(
                    "Deletar",
                    "deletar",
                    pad=((70, 0), (20, 0)),
                    cor="red",
                ),
            ]
        )

        self.atualiza_tela(layout)

        acao, _ = self.abrir()
        self.fechar()

        return acao

    def listar_logs(self, logs):
        layout = [[self.titulo("Logs")]]

        for log in logs:
            layout.append([self.texto(f"- {log.msg}. Data: {log.data}", size=(100, 1))])

        layout.append([self.botao("Voltar", "voltar", pad=((0, 0), (30, 0)))])

        self.atualiza_tela(layout)
        self.abrir()
        self.fechar()
