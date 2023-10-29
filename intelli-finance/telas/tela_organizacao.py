from tela_base import Tela
import re

import PySimpleGUI as sg


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
        extra = {}
        layout.append([self.texto("Despesas:")])
        if not despesas:
            extra["size"] = (400, 200)
            layout.append([
                [self.texto("Sua organização não possui nenhuma despesa.")]
        ]) 
        else:
            for despesa in despesas:
                sub_layout = [
                    [[self.texto(f"{despesa.valor} -> {despesa.categoria}", size=(60, 1))]]
                ]
                layout.append(sub_layout)

        layout.append([self.texto("Receitas:")])
        if not receitas:
            extra["size"] = (400, 200)
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
            self.botao("Adicionar Registro", "add", pad=((0, 0), (55, 0)))
        ]

        layout.append([botoes])

        self.atualiza_tela(layout, extra)
        acao, _ = self.abrir()
        self.fechar()

        return acao
    
    def adicionar_registro_financeiro(self):

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
                [sg.Radio("Receita", "RADIO1", default=True, key="Receita"), sg.Radio("Despesa", "RADIO1", key="Despesa")], 
                [self.texto("Categoria:"), sg.Combo(["Vendas Feira", "Pagamento Salários", "Reforma Fachada"], default_value="Pagamento Salários", size=(20, 1), key="categoria")],
                [self.texto("Valor:"), self.input("valor")],       
                [self.texto("Descrição:")],
                [sg.Multiline("", size=(25, 3), key="descricao")],
                [self.texto('Data:'), sg.InputText('', key='data')],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Salvar", "salvar", pad=((85, 0), (35, 10))),
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

        if acao == "salvar":

            # Verifica se existem dados faltando
            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")
                print(dados.values(), "values")
                return self.adicionar_registro_financeiro()
            
            # Verifica a validade da data
            if not validar_data(dados['data']):
                self.popup("A data precisa estar no formato dd/mm/aaaa.")
                return self.adicionar_registro_financeiro()

            # Verifica a validade do valor
            if not validar_valor(dados['valor']):
                self.popup("O valor precisa ser um número.")
                return self.adicionar_registro_financeiro()
            
            return dados

if __name__ == "__main__":
    tela_org = TelaOrganizacao()
    org_data = tela_org.adicionar_registro_financeiro()
    print(org_data)