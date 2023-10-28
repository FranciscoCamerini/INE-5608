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
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (55, 0))),
                    self.botao(
                        "Deletar Organização",
                        "deletar",
                        pad=((65, 25), (55, 0)),
                        cor="red",
                    ),
                    self.botao("Salvar", "salvar", pad=((0, 0), (55, 0))),
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
    