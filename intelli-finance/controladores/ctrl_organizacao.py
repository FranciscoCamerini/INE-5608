from telas.tela_organizacao import TelaOrganizacao
from bd.banco import Banco
from modelos.organizacao import Organizacao


class ControladorOrganizacao:
    def __init__(self):
        self.__tela = TelaOrganizacao()
        self.__banco = Banco()

    def cadastra_organizacao(self, cb=None):
        if dados := self.__tela.criar_organizacao():
            if self.__banco.pega_organizacao(dados["nome"]):
                self.__tela.popup("Esta organização já foi cadastrada!")

                return self.cadastra_organizacao(cb)

            organizacao = Organizacao(
                dados["nome"], dados["descrição"]
            )
            self.__banco.inclui_organizacao(organizacao)
            self.__tela.popup("Organização cadastrada com sucesso!")

        cb()

    def edita_organizacao(self, cb=None):
        pass
