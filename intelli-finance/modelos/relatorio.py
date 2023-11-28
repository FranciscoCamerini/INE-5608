from .usuario import Usuario


class Relatorio:
    def __init__(
        self,
        nome: str,
        data_inicio: str,
        data_fim: str,
        agrupar: str,
        categorias_receita: str,
        categorias_despesa: str,
        autor: Usuario,
    ):
        self.__nome = nome
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__agrupar = agrupar
        self.__categorias_receita = categorias_receita
        self.__categorias_despesa = categorias_despesa
        self.__autor = autor

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
        ...
