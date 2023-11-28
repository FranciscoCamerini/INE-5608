import csv
from datetime import datetime
from pathlib import Path

from .usuario import Usuario


PATH_RELATORIOS = Path(__file__).absolute().parent.parent.parent / "relatorios"


class Relatorio:
    def __init__(
        self,
        organizacao,
        nome: str,
        data_inicio: str,
        data_fim: str,
        agrupar: str,
        categorias_receita: [str],
        categorias_despesa: [str],
        autor: Usuario,
    ):
        self.__organizacao = organizacao
        self.__nome = nome
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__agrupar = agrupar
        self.__categorias_receita = categorias_receita
        self.__categorias_despesa = categorias_despesa
        self.__autor = autor

    @property
    def organizacao(self):
        return self.__organizacao

    @property
    def nome(self):
        return self.__nome

    @property
    def data_inicio(self):
        return self.__data_inicio

    @property
    def data_fim(self):
        return self.__data_fim

    @property
    def agrupar(self):
        return self.__agrupar

    @property
    def categorias_receita(self):
        return self.__categorias_receita

    @property
    def categorias_despesa(self):
        return self.__categorias_despesa

    @property
    def autor(self):
        return self.__autor

    def exportar(self):
        from telas.tela_organizacao import valida_data

        receitas = self.organizacao.receitas_por_categoria(self.categorias_receita)
        despesas = self.organizacao.despesas_por_categoria(self.categorias_despesa)

        nome_arquivo = (
            f"{self.nome}, {datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M')}.csv"
        )
        Path(PATH_RELATORIOS / nome_arquivo).touch()

        data_inicio = valida_data(self.data_inicio)
        data_fim = valida_data(self.data_fim)

        with open(PATH_RELATORIOS / nome_arquivo, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Data", "Tipo", "Categoria", "Descricao", "Valor"])
            valor_total = 0

            for receita in receitas:
                data = valida_data(receita.data)

                if data < data_inicio or data > data_fim:
                    continue

                writer.writerow(
                    [
                        receita.data,
                        "Receita",
                        receita.categoria,
                        receita.descricao,
                        receita.valor,
                    ]
                )
                valor_total += receita.valor

            for despesa in despesas:
                data = valida_data(despesa.data)

                if data < data_inicio or data > data_fim:
                    continue

                writer.writerow(
                    [
                        despesa.data,
                        "Despesa",
                        despesa.categoria,
                        despesa.descricao,
                        despesa.valor,
                    ]
                )
                valor_total += despesa.valor

            writer.writerow(["", "", "", "", "Valor Total"])
            writer.writerow(["", "", "", "", valor_total])
