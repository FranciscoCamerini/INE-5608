import os
import pickle
from pathlib import Path

from modelos.usuario import Usuario
from modelos.organizacao import Organizacao


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

    def pega_usuario(self, email: str) -> Usuario | None:
        return self.__pega_tabela("usuario").get(email)

    def pega_organizacao(self, nome: str) -> Organizacao | None:
        return self.__pega_tabela("organizacao").get(nome)

    def inclui_usuario(self, usuario: Usuario):
        usuarios = self.__pega_tabela("usuario")
        usuarios[usuario.email] = usuario.dados_cadastro()
        self.__atualiza_tabela("usuario", usuarios)

    def inclui_organizacao(self, org: Organizacao):
        organizacoes = self.__pega_tabela("organizacao")
        organizacoes[org.nome] = org.dados_organizacao()
        self.__atualiza_tabela("organizacao", organizacoes)