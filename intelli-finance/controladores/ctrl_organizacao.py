from telas.tela_organizacao import TelaOrganizacao
from bd.banco import Banco
from modelos.organizacao import Organizacao
from modelos.usuario import Usuario


class ControladorOrganizacao:
    def __init__(self):
        self.__tela = TelaOrganizacao()
        self.__banco = Banco()

    def cadastra_organizacao(self, usuario: Usuario, cb=None):
        if dados := self.__tela.criar_organizacao():
            if self.__banco.pega_organizacao(dados["nome"]):
                self.__tela.popup("Esta organização já foi cadastrada!")

                return self.cadastra_organizacao(usuario, cb)

            organizacao = Organizacao(dados["nome"], dados["descrição"])
            organizacao.define_proprietario(usuario)
            self.__banco.inclui_organizacao(organizacao)
            self.__tela.popup("Organização cadastrada com sucesso!")

        return cb(usuario)

    def listar_usuarios_org(self, usuario: Usuario, org: Organizacao, cb=None):
        acao = self.__tela.listar_usuarios(org.dados_organizacao())
        if acao == "add":
            acao, dados = self.__tela.adicionar_usuario()
            if acao == "confirmar":
                novo_usuario = self.__banco.pega_usuario(dados["email"])
                if not novo_usuario:
                    self.__tela.popup("Usuário Inexistente")

                if dados["status"] == "administrador":
                    org.adiciona_administrador(novo_usuario)
                elif dados["status"] == "funcionario_restrito":
                    org.adiciona_funcionario_restrito(novo_usuario)

                self.__banco.altera_organizacao(org.nome, org)
                self.__tela.popup("Usuário adicionado!")

            return self.listar_usuarios_org(usuario, org, cb)
        elif "@" in acao:
            usuario_editar = self.__banco.pega_usuario(acao)

            status = org.status_usuario(usuario_editar)
            acao, dados = self.__tela.edita_status_usuario(
                usuario_editar.dados_cadastro(),
                status,
            )

            novo_status = dados["status"]
            if acao == "confirmar":
                if novo_status != status:
                    if novo_status == "administrador":
                        org.adiciona_administrador(usuario_editar)
                    elif novo_status == "funcionario_restrito":
                        org.adiciona_funcionario_restrito(usuario_editar)

                    self.__banco.altera_organizacao(org.nome, org)
                    self.__tela.popup("Status de usuário alterado com sucesso!")
            elif acao == "remover":
                org.remove_usuario(usuario_editar)
                self.__banco.altera_organizacao(org.nome, org)
                self.__tela.popup("Usuário removido com sucesso!")

            return self.listar_usuarios_org(usuario, org, cb)

        self.edita_organizacao(usuario, org.nome, cb)

    def edita_organizacao(self, usuario: Usuario, nome_org: str, cb=None):
        org = self.__banco.pega_organizacao(nome_org)
        acao, dados = self.__tela.editar_organizacao(org.dados_organizacao())

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

        return cb(usuario)
