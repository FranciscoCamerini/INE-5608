class Organizacao:
    def __init__(self, nome, descricao):
        self.__nome: str = nome
        self.__descricao: str = descricao
        

    @property
    def nome(self):
        return self.__nome

    def dados_organizacao(self):
        return {
            "nome": self.__nome,
            "descricao": self.__descricao
        }
