from telas.tela_organizacao import TelaOrganizacao
from bd.banco import Banco
from modelos.organizacao import Organizacao
from modelos.usuario import Usuario
from modelos.categoria import Categoria


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
                        Categoria(dados['nome'], dados['categoria'], dados['descricao'])
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
        org = self.__banco.pega_organizacao(nome_org)
        acao, dados = self.__tela.editar_organizacao(
            org.dados_organizacao(), org.status_usuario(usuario)
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

        return cb(usuario)
