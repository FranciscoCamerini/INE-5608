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
        if acao == "criar":


            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.criar_organizacao()

            return dados
        
        self.fechar()
       
        

    def editar_organizacao(self):
        self.atualiza_tela(
            [
                [self.texto("Nome da Organização:"), self.input("nome")],
               
                [self.texto("Descrição:")],
                [self.input_grande("descrição")],
                [
                    self.botao("Cancelar", "cancelar", pad=((0, 0), (35, 10))),
                    self.botao("Deletar", "confirmar", pad=((85, 0), (35, 10))),
                    self.botao("Confirmar", "confirmar", pad=((85, 0), (35, 10))),
                ],
            ]
        )
        acao, dados = self.abrir()
        if acao == "confirmar":


            if any(not dado for dado in dados.values()):
                self.popup("Favor preencher todos os campos!")

                return self.criar_organizacao()

            return dados
        
        self.fechar()
    
