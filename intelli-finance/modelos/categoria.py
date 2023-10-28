class Categoria:
    def __init__(self, nome: str, tipo: str, descricao: str) -> None:
        self.__nome = nome
        self.__descricao = descricao
        self.__tipo = tipo

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, tipo: str):
        self.__tipo = tipo
