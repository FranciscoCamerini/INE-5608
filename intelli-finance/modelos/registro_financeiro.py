class RegistroFinanceiro:
    def __init__(
        self, data: str, descricao: str, valor: float, tipo: str, categoria: str
    ) -> None:
        self.__data = data
        self.__descricao = descricao
        self.__valor = valor
        self.__tipo = tipo
        self.__categoria = categoria

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: str):
        self.__data = data

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor: str):
        self.__valor = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: str):
        self.__tipo = tipo

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: str):
        self.__categoria = categoria

    def dados(self):
        return {
            "data": self.data,
            "descricao": self.descricao,
            "valor": self.valor,
            "categoria": self.categoria,
        }
