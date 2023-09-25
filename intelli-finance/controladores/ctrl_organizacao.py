from telas.tela_organizacao import TelaOrganizacao
from bd.banco import Banco
from modelos.organizacao import Organizacao


class ControladorOrganizacao:
    def __init__(self):
        self.__tela = TelaOrganizacao()
        self.__banco = Banco()

    def cadastra_organizacao(self, usuario, cb=None):
        if dados := self.__tela.criar_organizacao():
            if self.__banco.pega_organizacao(dados["nome"]):
                self.__tela.popup("Esta organização já foi cadastrada!")

                return self.cadastra_organizacao(usuario, cb)

            organizacao = Organizacao(dados["nome"], dados["descrição"])
            organizacao.define_proprietario(usuario)
            self.__banco.inclui_organizacao(organizacao)
            self.__tela.popup("Organização cadastrada com sucesso!")

        return cb(usuario)

    def edita_organizacao(self, usuario, nome_org, cb=None):
        org = self.__banco.pega_organizacao(nome_org)
        acao, dados = self.__tela.editar_organizacao(org.dados_organizacao())
        if acao == "salvar":
            organizacao = Organizacao(dados["nome"], dados["descrição"])
            organizacao.define_proprietario(usuario)
            self.__banco.altera_organizacao(nome_org, organizacao)
            self.__tela.popup("Organização alterada com sucesso!")
        elif acao == "deletar":
            self.__banco.deleta_organizacao(nome_org)
            self.__tela.popup("Organização deletada com sucesso!")

        return cb(usuario)
