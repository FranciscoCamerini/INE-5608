from telas.tela_base import Tela
import re

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

    def editar_organizacao(self, dados, status_usuario):
        pode_alterar_dados = status_usuario == "proprietario"

        botoes = [
            self.botao("Voltar", "cancelar", pad=((0, 20), (55, 0))),
            self.botao("Usuários", "usuarios", pad=((0, 0), (55, 0))),
            self.botao("Categorias", "categorias", pad=((20, 0), (55, 0))),
            self.botao("Registros", "registros", pad=((20, 0), (55, 0))),
        ]

        if pode_alterar_dados:
            botoes.append(self.botao("Salvar", "salvar", pad=((55, 0), (55, 0))))
            botoes.insert(
                3,
                self.botao(
                    "Deletar Organização",
                    "deletar",
                    pad=((65, 25), (55, 0)),
                    cor="red",
                ),
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
                [self.texto("Sua organização não possui categorias de transação.")]
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
        func_restritos = dados["funcionarios_restritos"]
        administradores = dados["administradores"]

        proprietario = status_usuario == "proprietario"

        layout = []
        extra = {}
        if not (func_restritos or administradores):
            extra["size"] = (400, 200)
            layout.append(
                [self.texto("Sua organização ainda não possui outros membros.")]
            )

        if func_restritos:
            layout.append([self.titulo("Funcionários restritos:")])
            for usuario in func_restritos:
                sub_layout = [
                    [[self.texto(usuario.nome)], [self.texto(usuario.email)]],
                ]
                if proprietario:
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
                if proprietario:
                    sub_layout.append(
                        self.botao("Editar", usuario.email, pad=((0, 0), (0, 40)))
                    )
                layout.append(sub_layout)

        botoes = [
            self.botao("Voltar", "voltar", pad=((0, 20), (55, 0))),
        ]
        if proprietario:
            botoes.append(self.botao("Adicionar Usuário", "add", pad=((0, 0), (55, 0))))

        layout.append([botoes])

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
    
    def listar_registros_financeiros(self, dados: dict):
        despesas = dados["despesas"]
        receitas = dados["receitas"]
        layout = []
        print(dados, "dados")
        print(despesas, "despesas")
        print(receitas, "receitas")
        
        layout.append([self.texto("Despesas:")])
        if not despesas:
           
            layout.append([
                [self.texto("Sua organização não possui nenhuma despesa.")]
        ]) 
        else:
            for despesa in despesas:
                sub_layout = [
                    [[self.texto(f"{despesa.valor} -> {despesa.categoria}")]]
                ]
                layout.append(sub_layout)

        layout.append([self.texto("Receitas:")])
        if not receitas:
            
            layout.append([
                [self.texto("Sua organização não possui nenhuma receita.")]
        ]) 
        else:
            for receita in receitas:
                sub_layout = [
                    [[self.texto(f"{receita.valor} -> {receita.categoria}", size=(60, 1))]]
                ]
                layout.append(sub_layout)
        
        botoes = [
            self.botao("Voltar", "voltar", pad=((0, 50), (55, 0))),
             self.botao("Adicionar Despesa", "addDespesa", pad=((0, 0), (55, 0))),
            self.botao("Adicionar Receita", "addReceita", pad=((0, 0), (55, 0)))
           
        ]

        layout.append([botoes])

        self.atualiza_tela(layout)
        acao, _ = self.abrir()
        self.fechar()

        return acao
    
    def adicionar_registro_financeiro(self, categorias_org, tipo):
        categorias = []
        for cat in categorias_org:
            print(f"Nome: {cat.nome}, Tipo: {cat.tipo}")
        
        if (tipo == "receita"):
            for cat in categorias_org:
                categorias.append(cat.nome)
        
        else:
             for cat in categorias_org:
                categorias.append(cat.nome)
        

        def validar_data(data: str) -> bool:
            """Valida se a data está no formato dd/mm/aaaa."""
            pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
            return bool(pattern.match(data))
        
        def validar_valor(valor: str) -> bool:
            """Valida se o valor é um número."""
            pattern = re.compile(r'^\d+(\.\d+)?$')
            return bool(pattern.match(valor))
       
        self.atualiza_tela(
            [
                [self.texto("Tipo:")],
                [self.radio("Receita", "RADIO1", default=(tipo == "receita"), key="Receita", disabled=True), self.radio("Despesa", "RADIO1", default=(tipo == "despesa"), key="Despesa", disabled=True)], 
                [self.texto("Categoria:"), self.combo(categorias, valor_default=categorias[0], tamanho=(20, 1), chave="categoria", readonly=True)],
                [self.texto("Valor:"), self.input("valor")],       
                [self.texto("Descrição:")],
                [self.multiline("", tamanho=(25, 3), chave="descricao")],
                [self.texto('Data:'), self.input("data")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
                ],
            ]
        )
        acao, dados = self.abrir()
        self.fechar()

        # Determina o tipo e depois exclui as chaves indesejadas
        if dados.get("Receita"):
            dados['tipo'] = "Receita"
        else:
            dados['tipo'] = "Despesa"
        del dados["Receita"]
        del dados["Despesa"]

        if acao == "confirmar":

            # Verifica se existem dados faltando
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")
                print(dados.values(), "values")
                return self.adicionar_registro_financeiro(categorias_org, tipo)
            
            # Verifica a validade do valor
            if not validar_valor(dados['valor']):
                self.popup("O valor deve conter somente números.")
                return self.adicionar_registro_financeiro(categorias_org, tipo)
            
            # Verifica a validade da data
            if not validar_data(dados['data']):
                print(dados, "dados")
                self.popup("A data deve estar no formato dd/mm/aaaa.")
                return self.adicionar_registro_financeiro(categorias_org, tipo)
            
            
        return acao, dados


   