CHAVE = "9a8f5c84d8e7b5a13c1dfe842dbf6b4a"


class Usuario:
    def __init__(self, nome, email, sobre, senha):
        self.__nome: str = nome
        self.__email: str = email
        self.__sobre: str = sobre
        self.__senha = senha

    @property
    def email(self):
        return self.__email

    @property
    def nome(self):
        return self.__nome

    def valida_senha(self, senha):
        return self.__senha == senha

    def dados_cadastro(self):
        return {
            "senha": self.__senha,
            "nome": self.__nome,
            "email": self.__email,
            "sobre": self.__sobre,
        }