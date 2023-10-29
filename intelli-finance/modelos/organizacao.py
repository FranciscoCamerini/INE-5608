from modelos.usuario import Usuario
from modelos.categoria import Categoria
from modelos.registro_financeiro import RegistroFinanceiro


class Organizacao:
    def __init__(self, nome, descricao):
        self.__nome: str = nome
        self.__descricao: str = descricao
        self.__proprietario: Usuario = None
        self.__administradores: list[Usuario] = []
        self.__funcionarios_restritos: list[Usuario] = []
        self.__categorias: list[Categoria] = []
        self.__despesas: list[RegistroFinanceiro]
        self.__receitas: list[RegistroFinanceiro]

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__nome = descricao

    @property
    def proprietario(self):
        return self.__proprietario

    def status_usuario(self, usuario):
        if self.proprietario.email == usuario.email:
            return "proprietario"
        elif usuario.email in [u.email for u in self.__administradores]:
            return "administrador"
        elif usuario.email in [u.email for u in self.__funcionarios_restritos]:
            return "funcionario_restrito"

    def define_proprietario(self, usuario: Usuario):
        self.__proprietario = usuario

    def adiciona_administrador(self, usuario: Usuario):
        for func in self.__funcionarios_restritos:
            if func.email == usuario.email:
                self.__funcionarios_restritos.remove(func)

        self.__administradores.append(usuario)

    def adiciona_funcionario_restrito(self, usuario: Usuario):
        for adm in self.__administradores:
            if adm.email == usuario.email:
                self.__administradores.remove(adm)

        self.__funcionarios_restritos.append(usuario)

    def remove_usuario(self, usuario):
        for adm in self.__administradores:
            if adm.email == usuario.email:
                self.__administradores.remove(adm)
                return

        for func in self.__funcionarios_restritos:
            if func.email == usuario.email:
                self.__funcionarios_restritos.remove(func)
                return

    def adiciona_categoria(self, categoria: Categoria):
        for categ in self.__categorias:
            if categ.nome == categoria.nome:
                raise FileExistsError
        else:
            self.__categorias.append(categoria)

    def remove_categoria(self, categoria: Categoria):
        self.__categorias.remove(categoria)

    def adiciona_despesa(self, despesa: RegistroFinanceiro):
        self.__despesas.append(despesa)

    def adiciona_receita(self, receita: RegistroFinanceiro):
        self.__receitas.append(receita)

    def dados_organizacao(self):
        return {
            "nome": self.__nome,
            "descricao": self.__descricao,
            "proprietario": self.__proprietario,
            "administradores": self.__administradores,
            "funcionarios_restritos": self.__funcionarios_restritos,
            "categorias": self.__categorias,
            "despesas": self.__despesas,
            "receitas": self.__receitas

        }
