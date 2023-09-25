from modelos.usuario import Usuario


class Organizacao:
    def __init__(self, nome, descricao):
        self.__nome: str = nome
        self.__descricao: str = descricao
        self.__proprietario: Usuario = None
        self.__administradores: list[Usuario] = []
        self.__funcionarios_restritos: list[Usuario] = []

    @property
    def nome(self):
        return self.__nome

    @property
    def proprietario(self):
        return self.__proprietario

    def status_usuario(self, usuario):
        if self.proprietario.email == usuario.email:
            return "proprietario"
        elif usuario in self.__administradores:
            return "administrador"
        elif usuario in self.__funcionarios_restritos:
            return "funcionario_restrito"

    def define_proprietario(self, usuario: Usuario):
        self.__proprietario = usuario

    def adiciona_administrador(self, usuario: Usuario):
        self.__administradores.append(usuario)

    def adiciona_funcionario_restrito(self, usuario: Usuario):
        self.__funcionarios_restritos.append(usuario)

    def dados_organizacao(self):
        return {
            "nome": self.__nome,
            "descricao": self.__descricao,
            "proprietario": self.__proprietario,
            "administradores": self.__administradores,
            "funcionarios_restritos": self.__funcionarios_restritos,
        }
