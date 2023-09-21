class Usuario:
    def __init__(self, nome, email, sobre, senha):
        self.__nome: str = nome
        self.__email: str = email
        self.__sobre: str = sobre
        self.__senha: str = senha

    @property
    def email(self):
        return self.__email

    def dados_cadastro(self):
        return {
            "senha": self.__senha,
            "nome": self.__nome,
            "email": self.__email,
            "sobre": self.__sobre,
        }
