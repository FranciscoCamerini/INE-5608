class Log:
    def __init__(self, data, msg, usuario, extra={}):
        self.__data = data
        self.__msg = msg
        self.__usuario = usuario
        self.__extra = extra

    @property
    def data(self):
        return self.__data

    @property
    def msg(self):
        return self.__msg

    @property
    def usuario(self):
        return self.__usuario

    @property
    def extra(self):
        return self.__extra
