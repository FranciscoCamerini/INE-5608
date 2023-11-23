from telas.tela_organizacao import TelaOrganizacao
from bd.banco import Banco
from modelos.organizacao import Organizacao
from modelos.usuario import Usuario
from modelos.categoria import Categoria
from modelos.relatorio import Relatorio
from modelos.registro_financeiro import RegistroFinanceiro


class ControladorOrganizacao:
    def __init__(self):
        self.__tela = TelaOrganizacao()
        self.__banco = Banco()

    def cadastra_organizacao(self, usuario: Usuario, cb=None):
        if dados := self.__tela.criar_organizacao():
            if self.__banco.pega_organizacao(dados["nome"]):
                self.__tela.popup("Esta organização já foi cadastrada!")

                return self.cadastra_organizacao(usuario, cb)

            organizacao = Organizacao(dados["nome"], dados["descricao"])
            organizacao.define_proprietario(usuario)
            self.__banco.salva_organizacao(organizacao)
            self.__tela.popup("Organização cadastrada com sucesso!")

        return cb(usuario)

    def adicionar_usuario(self, org, proprietario):
        acao, dados = self.__tela.pega_dados_adicionar_usuario()
        if acao == "confirmar":
            senha_valida = proprietario.valida_senha(dados["senha"])
            if not senha_valida:
                self.__tela.popup("Senha incorreta!")
                return

            novo_usuario = self.__banco.pega_usuario(dados["email"])
            if not novo_usuario:
                self.__tela.popup("Usuário Inexistente!")
                return

            stauts_atual = org.status_usuario(novo_usuario)
            if stauts_atual:
                self.__tela.popup("Usuário já membro da Organização!")
                return

            if dados["status"] == "administrador":
                org.adiciona_administrador(novo_usuario)
            elif dados["status"] == "funcionario_restrito":
                org.adiciona_funcionario_restrito(novo_usuario)

            self.__banco.salva_organizacao(org)
            self.__tela.popup("Usuário adicionado!")

    def editar_usuario(self, proprietario, org, email):
        usuario_editar = self.__banco.pega_usuario(email)

        status = org.status_usuario(usuario_editar)
        dados_usuario = usuario_editar.dados_cadastro()
        acao, dados = self.__tela.edita_status_usuario(
            dados_usuario,
            status,
        )

        senha_valida = proprietario.valida_senha(dados["senha"])
        if not senha_valida:
            self.__tela.popup("Senha incorreta!")
            return

        if acao == "confirmar":
            status_atual = org.status_usuario(usuario_editar)
            if dados["status"] != status_atual:
                if dados["status"] == "administrador":
                    org.adiciona_administrador(usuario_editar)
                elif dados["status"] == "funcionario_restrito":
                    org.adiciona_funcionario_restrito(usuario_editar)

                self.__banco.salva_organizacao(org)
                self.__tela.popup("Status de usuário alterado com sucesso!")
        elif acao == "remover":
            org.remove_usuario(usuario_editar)

            self.__banco.salva_organizacao(org)
            self.__tela.popup("Usuário removido com sucesso!")

    def listar_usuarios_org(self, usuario: Usuario, org: Organizacao, cb=None):
        acao = self.__tela.listar_usuarios(
            org.dados_organizacao(), org.status_usuario(usuario)
        )
        if acao == "add":
            self.adicionar_usuario(org, usuario)

            return self.listar_usuarios_org(usuario, org, cb)
        elif "@" in acao:
            self.editar_usuario(usuario, org, acao)

            return self.listar_usuarios_org(usuario, org, cb)

        self.edita_organizacao(usuario, org.nome, cb)

    def listar_categorias_org(self, usuario: Usuario, org: Organizacao, cb=None):
        acao = self.__tela.listar_categorias(
            org.dados_organizacao(), org.status_usuario(usuario)
        )
        if acao == "add":
            acao, dados = self.__tela.adicionar_categoria()
            # dados = {'nome': str, categoria: 'Receita' || 'Despesa', 'descricao': str}
            if acao == "confirmar":
                try:
                    org.adiciona_categoria(
                        Categoria(dados["nome"], dados["categoria"], dados["descricao"])
                    )
                except FileExistsError:
                    self.__tela.popup(
                        f"Já existe uma categoria com nome '{dados['nome']}'"
                    )
                else:
                    self.__tela.popup("Categoria adicionado!")
                self.__banco.altera_organizacao(org.nome, org)

            return self.listar_categorias_org(usuario, org, cb)

        self.edita_organizacao(usuario, org.nome, cb)

    def edita_organizacao(self, usuario: Usuario, nome_org: str, cb=None):
        org: Organizacao = self.__banco.pega_organizacao(nome_org)

        notificacoes = org.registros_a_notificar()
        acao, dados = self.__tela.editar_organizacao(
            org.dados_organizacao(), org.status_usuario(usuario), notificacoes
        )

        match acao:
            case "salvar":
                if nome_org != dados["nome"]:
                    if self.__banco.pega_organizacao(dados["nome"]):
                        self.__tela.popup("Já há uma organização com este nome!")
                        return self.edita_organizacao(usuario, nome_org, cb)
                else:
                    self.__banco.deleta_organizacao(nome_org)

                org.nome = dados["nome"]
                org.descricao = dados["descricao"]
                self.__banco.altera_organizacao(org.nome, org)
                self.__tela.popup("Organização alterada com sucesso!")
            case "usuarios":
                return self.listar_usuarios_org(usuario, org, cb)
            case "deletar":
                self.__banco.deleta_organizacao(nome_org)
                self.__tela.popup("Organização deletada com sucesso!")
            case "categorias":
                return self.listar_categorias_org(usuario, org, cb)
            case "registros":
                return self.listar_registros_financeiros_org(usuario, org, cb)
            case "notificacoes":
                return self.listar_notificacoes(usuario, org, notificacoes, cb)
            case "relatorio":
                return self.listar_relatorios(usuario, org, cb)

        return cb(usuario)

    def listar_registros_financeiros_org(
        self, usuario: Usuario, org: Organizacao, cb=None
    ):
        dados_org = org.dados_organizacao()
        acao = self.__tela.listar_registros_financeiros(
            org.status_usuario(usuario), dados_org
        )
        receitas_org = dados_org["receitas"]
        despesas_org = dados_org["despesas"]

        categorias_org = org.dados_organizacao()["categorias"]
        categorias_despesa = [cat for cat in categorias_org if cat.tipo == "Despesa"]
        categorias_receita = [cat for cat in categorias_org if cat.tipo == "Receita"]

        if acao == "addDespesa":
            if not categorias_despesa:  # Se a lista de categorias está vazia
                self.__tela.popup("Não há categorias de despesa disponíveis.")
                return self.listar_registros_financeiros_org(usuario, org, cb)

            acao, dados = self.__tela.adicionar_registro_financeiro(
                categorias_org, "despesa"
            )

            if acao == "confirmar":
                org.adiciona_despesa(
                    RegistroFinanceiro(
                        dados["data"],
                        dados["descricao"],
                        abs(float(dados["valor"])) * -1,
                        dados["tipo"],
                        dados["categoria"],
                        org.status_usuario(usuario),
                    )
                )

                self.__tela.popup("Despesa adicionada!")
                self.__banco.altera_organizacao(org.nome, org)

            return self.listar_registros_financeiros_org(usuario, org, cb)

        elif acao == "addReceita":
            if not categorias_receita:  # Se a lista de categorias está vazia
                self.__tela.popup("Não há categorias de receita disponíveis.")
                return self.listar_registros_financeiros_org(usuario, org, cb)

            acao, dados = self.__tela.adicionar_registro_financeiro(
                categorias_org, "receita"
            )

            if acao == "confirmar":
                org.adiciona_receita(
                    RegistroFinanceiro(
                        dados["data"],
                        dados["descricao"],
                        abs(float(dados["valor"])),
                        dados["tipo"],
                        dados["categoria"],
                        org.status_usuario(usuario),
                    )
                )

                self.__tela.popup("Receita adicionada!")
                self.__banco.altera_organizacao(org.nome, org)

            return self.listar_registros_financeiros_org(usuario, org, cb)

        elif "editar_despesa" in acao:
            index = int(acao.split(":")[1])

            registro: RegistroFinanceiro = despesas_org[index]

            acao, dados = self.__tela.adicionar_registro_financeiro(
                categorias_org, "despesa", dados_input=registro.dados()
            )
            if acao == "confirmar":
                registro.categoria = dados["categoria"]
                registro.valor = abs(float(dados["valor"])) * -1
                registro.descricao = dados["descricao"]
                registro.data = dados["data"]

                despesas_org[index] = registro
                org.despesas = despesas_org
                self.__banco.salva_organizacao(org)
                self.__tela.popup("Registro alterado com sucesso!")
            elif acao == "deletar":
                despesas_org.pop(index)
                org.despesas = despesas_org
                self.__banco.salva_organizacao(org)
                self.__tela.popup("Registro removido com sucesso!")

            return self.listar_registros_financeiros_org(usuario, org, cb)

        elif "editar_receita" in acao:
            index = int(acao.split(":")[1])

            registro: RegistroFinanceiro = receitas_org[index]

            acao, dados = self.__tela.adicionar_registro_financeiro(
                categorias_org, "receita", dados_input=registro.dados()
            )
            if acao == "confirmar":
                registro.categoria = dados["categoria"]
                registro.valor = abs(float(dados["valor"]))
                registro.descricao = dados["descricao"]
                registro.data = dados["data"]

                receitas_org[index] = registro
                org.receitas = receitas_org
                self.__banco.salva_organizacao(org)
                self.__tela.popup("Registro alterado com sucesso!")
            elif acao == "deletar":
                receitas_org.pop(index)
                org.receitas = receitas_org
                self.__banco.salva_organizacao(org)
                self.__tela.popup("Registro removido com sucesso!")

            return self.listar_registros_financeiros_org(usuario, org, cb)

        self.edita_organizacao(usuario, org.nome, cb)

    def listar_notificacoes(self, usuario, org, notificacoes, cb):
        self.__tela.listar_notificacoes(notificacoes)

        self.edita_organizacao(usuario, org.nome, cb)

    def listar_relatorios(self, usuario: Usuario, org: Organizacao, cb, listar=True):
        categorias_despesa = [c.nome for c in org.categorias if c.tipo == "Despesa"]
        categorias_receita = [c.nome for c in org.categorias if c.tipo == "Receita"]

        acao, dados = self.__tela.pega_dados_relatorio(
            org.relatorios, categorias_receita, categorias_despesa, listar=listar
        )

        if acao == "gerar":
            if not usuario.valida_senha(dados["senha"]):
                self.__tela.popup("Senha inválida!")
                return self.listar_relatorios(usuario, org, cb, listar=False)

            if dados["nome"] in [relatorio.nome for relatorio in org.relatorios]:
                self.__tela.popup(
                    "Já há um relatório com este nome na sua organização!"
                )
                return self.listar_relatorios(usuario, org, cb, listar=False)

            dados.pop("senha", None)
            relatorio = Relatorio(**dados, autor=usuario)
            org.relatorios.append(relatorio)
            self.__banco.salva_organizacao(org)
            self.__tela.popup("Relatório criado com sucesso!")

            return self.listar_relatorios(usuario, org, cb)

        self.edita_organizacao(usuario, org.nome, cb)
