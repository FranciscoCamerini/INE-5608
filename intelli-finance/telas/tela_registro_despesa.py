import re
import PySimpleGUI as sg

from telas.tela_base import Tela

class TelaDespesaReceita(Tela):
    def __init__(self):
        super().__init__()

    def validar_data(self, data: str) -> bool:
        """Valida se a data está no formato dd/mm/aaaa."""
        pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        return bool(pattern.match(data))
    
    def validar_valor(self, valor: str) -> bool:
        """Valida se o valor é um número."""
        pattern = re.compile(r'^\d+(\.\d+)?$')
        return bool(pattern.match(valor))

    def criar_despesa_receita(self) -> (dict, None):
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
                return self.criar_despesa_receita()
            
            # Verifica a validade da data
            if not self.validar_data(dados['data']):
                self.popup("A data precisa estar no formato dd/mm/aaaa!")
                return self.criar_despesa_receita()

            # Verifica a validade do valor
            if not self.validar_valor(dados['valor']):
                self.popup("Por favor, insira um valor numérico válido!")
                return self.criar_despesa_receita()
            
            return dados

# if __name__ == "__main__":
#     tela_org = TelaDespesaReceita()
#     org_data = tela_org.criar_despesa_receita()
#     print(org_data)
