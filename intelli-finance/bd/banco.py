import os
import pickle
from pathlib import Path

from modelos.organizacao import Organizacao
from modelos.usuario import Usuario


PATH_DADOS = Path(os.path.join(Path(__file__).parent.resolve(), "dados"))


class Banco:
    def __init__(self):
        if not Path.exists(PATH_DADOS):
            Path.touch(PATH_DADOS, exist_ok=True)
            with open(PATH_DADOS, "wb") as arquivo:
                pickle.dump({"usuario": {}, "organizacao": {}}, arquivo)

    def __pega_tabela(self, tabela) -> dict:
        with open(PATH_DADOS, "rb") as arquivo:
            dados = pickle.load(arquivo)

        return dados[tabela]

    def __atualiza_tabela(self, nome_tabela, tabela):
        with open(PATH_DADOS, "rb") as arquivo:
            dados = pickle.load(arquivo)

        dados[nome_tabela] = tabela

        with open(PATH_DADOS, "wb") as arquivo:
            pickle.dump(dados, arquivo)

    def pega_usuario(self, email: str):
        return self.__pega_tabela("usuario").get(email)

    def pega_organizacao(self, nome: str) -> Organizacao | None:
        return self.__pega_tabela("organizacao").get(nome)

    def inclui_usuario(self, usuario: Usuario):
        usuarios = self.__pega_tabela("usuario")
        usuarios[usuario.email] = usuario
        self.__atualiza_tabela("usuario", usuarios)

    def altera_usuario(self, email, usuario: Usuario):
        usuarios = self.__pega_tabela("usuario")
        usuarios.pop(email, None)
        usuarios[usuario.email] = usuario
        self.__atualiza_tabela("usuario", usuarios)

    def deleta_usuario(self, usuario):
        usuarios = self.__pega_tabela("organizacao")
        usuarios.pop(usuario.email, None)
        org_p, org_a, org_f = self.organizacoes_para_usuario(usuario)
        for org in org_p:
            self.deleta_organizacao(org.nome)
        for org in org_a:
            org.remove_usuario(usuario)
        for org in org_f:
            org.remove_usuario(usuario)

        self.__atualiza_tabela("usuario", usuarios)

    def salva_organizacao(self, org: Organizacao):
        organizacoes = self.__pega_tabela("organizacao")
        organizacoes[org.nome] = org
        self.__atualiza_tabela("organizacao", organizacoes)

    def altera_organizacao(self, nome_org: str, org: Organizacao):
        organizacoes = self.__pega_tabela("organizacao")
        organizacoes.pop(nome_org, None)
        organizacoes[org.nome] = org
        self.__atualiza_tabela("organizacao", organizacoes)

    def deleta_organizacao(self, nome: str):
        organizacoes = self.__pega_tabela("organizacao")
        organizacoes.pop(nome, None)
        self.__atualiza_tabela("organizacao", organizacoes)

    def organizacoes_para_usuario(self, usuario: Usuario):
        organizacoes = self.__pega_tabela("organizacao")
        organizacoes_p = []  # Organizacoes proprietario
        organizacoes_a = []  # Organizacoes admin
        organizacoes_f = []  # Organizacoes funcionario

        for org in organizacoes.values():
            status = org.status_usuario(usuario)
            match status:
                case "proprietario":
                    organizacoes_p.append(org)
                case "administrador":
                    organizacoes_a.append(org)
                case "funcionario_restrito":
                    organizacoes_f.append(org)

        return organizacoes_p, organizacoes_a, organizacoes_f
