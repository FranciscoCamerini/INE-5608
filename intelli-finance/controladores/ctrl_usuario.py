from telas.tela_usuario import TelaUsuario
from bd.banco import Banco
from modelos.usuario import Usuario
from controladores.ctrl_organizacao import ControladorOrganizacao


class ControladorUsuario:
    def __init__(self):
        self.__tela = TelaUsuario()
        self.__banco = Banco()
        self.__ctrl_org = ControladorOrganizacao()

    def realiza_cadastro(self, cb=None):
        acao, dados = self.__tela.cadastro_usuario()
        if acao == "confirmar" and dados:
            if self.__banco.pega_usuario(dados["email"]):
                self.__tela.popup("Este email já foi cadastrado!")

                return self.realiza_cadastro(cb)

            usuario = Usuario(
                dados["nome"], dados["email"], dados["sobre"], dados["senha1"]
            )
            self.__banco.inclui_usuario(usuario)
            self.__tela.popup("Usuário cadastrado com sucesso!")

        return cb()

    def login(self, cb=None):
        if dados := self.__tela.login_usuario():
            usuario = self.__banco.pega_usuario(dados["email"])
            if usuario:  # Usuário existe
                if usuario.valida_senha(dados["senha"]):  # Login efetuado com sucesso
                    return self.tela_principal(usuario)
                else:
                    self.__tela.popup("Senha incorreta")
                    return self.login(cb)
            else:  # Não existe usuário com este email
                self.__tela.popup(
                    "Não há cadastro com esse e-mail, por favor, tente novamente com outro e-mail ou cadastre esse."
                )
                return self.login(cb)
        if cb:
            return cb()

    def lista_organizacoes(self, usuario):
        (
            organizacoes_p,
            organizacoes_a,
            organizacoes_f,
        ) = self.__banco.organizacoes_para_usuario(usuario)
        acao, dados = self.__tela.organizacoes(
            organizacoes_p, organizacoes_a, organizacoes_f
        )
        match acao:
            case "criar_org":
                return self.__ctrl_org.cadastra_organizacao(
                    usuario, cb=self.lista_organizacoes
                )
            case "voltar":
                return self.tela_principal(usuario)

        if acao.startswith("editar-"):
            nome_org = acao.split("-")[1]
            self.__ctrl_org.edita_organizacao(
                usuario, nome_org, self.lista_organizacoes
            )

    def tela_principal(self, usuario):
        acao, dados = self.__tela.principal(usuario.nome)
        match acao:
            case "org":
                return self.lista_organizacoes(usuario)
            case "editar":
                return self.edita_cadastro(usuario, cb=self.tela_principal)
            case "logoff":
                return self.login()

    def edita_cadastro(self, usuario: Usuario, cb=None):
        acao, dados = self.__tela.cadastro_usuario(
            dados=usuario.dados_cadastro(),
            atualizacao=True,
        )
        if acao == "cancelar":
            return cb(usuario)

        if usuario and not usuario.valida_senha(dados["senha_atual"]):
            self.__tela.popup("A senha atual está incorreta.")
            return self.edita_cadastro(usuario, cb)

        if acao == "deletar":
            self.__banco.deleta_usuario(usuario)
            self.__tela.popup("Cadastro removido com sucesso!")
            return self.login()
        elif acao == "confirmar":
            senha = (
                dados["senha_atual"]
                if not dados.get("senha_nova")
                else dados.get("senha_nova")
            )
            usuario = Usuario(dados["nome"], usuario.email, dados["sobre"], senha)
            self.__banco.altera_usuario(usuario.email, usuario)

        return cb(usuario)
