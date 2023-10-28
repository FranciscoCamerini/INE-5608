import PySimpleGUI as sg
from abc import abstractmethod, ABC


DEFAULT_FONT = ("Arial", 16, "normal")


class Tela(ABC):
    @abstractmethod
    def __init__(self):
        sg.theme("Reddit")

    def popup(self, msg):
        sg.Popup("", msg, font=DEFAULT_FONT)

    def input(
        self,
        chave: str,
        valor: str = "",
        tamanho: tuple[int] = (35, 30),
        extra: dict = None,
    ):
        if not extra:
            extra = {}

        return sg.InputText(valor, key=chave, size=tamanho, **extra, font=DEFAULT_FONT)

    def input_grande(self, *args, **kwargs):
        return self.input(
            *args,
            **kwargs,
            tamanho=(35, 100),
            extra={"expand_x": True, "expand_y": True}
        )

    def input_senha(self, *args, **kwargs):
        return self.input(*args, **kwargs, extra={"password_char": "*"})

    def titulo(self, texto: str, alinhamento: str = "center"):
        return sg.Text(
            texto, justification=alinhamento, size=(40, 3), font=("arial", 24, "bold")
        )

    def texto(self, texto: str, estilo: str = "normal", size=(25, 1)):
        return sg.Text(texto, size=size, font=("arial", 16, estilo))

    def botao(self, texto_botao: str, chave: str, pad: int = 0, cor: str = "blue"):
        return sg.Button(
            texto_botao,
            key=chave,
            size=(16, 1),
            font=DEFAULT_FONT,
            border_width=2,
            pad=pad,
            button_color=cor,
        )

    def dropdown(self, escolhas: [str], default=None):
        return sg.Combo(escolhas, default, font=DEFAULT_FONT)

    def atualiza_tela(self, layout: dict, extra: dict = None):
        extra = {} if not extra else dict(extra)

        self.__window = sg.Window("Intelli-Finance", **extra).Layout(layout)

    def abrir(self):
        botao, valores = self.__window.Read()

        return botao, valores

    def fechar(self):
        self.__window.Close()

    def ler_input(self):
        return self.__window.Read()
