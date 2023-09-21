from telas.tela_base import Tela


class TelaInicial(Tela):
    def __init__(self):
        super().__init__()

    def opcoes(self):
        self.atualiza_tela(
            [
                [self.titulo("Bem Vindo(a) ao Intelli-Finance!")],
                [self.botao("Fazer Login", chave="logar")],
                [
                    self.botao(
                        "Cadastrar Usuário", chave="cadastrar", pad=((0, 0), (10, 60))
                    )
                ],
                [self.botao("Encerrar", chave="encerrar", pad=((0, 0), (0, 10)))],
            ],
            {"element_justification": "center"},
        )
        opcao, _ = self.ler_input()
        self.fechar()

        return opcao
