import sys

class Argumentos:
    def __init__(self):
        self.__argumentos = []

    def get(self):
        argumentos = {}
        args = sys.argv
        for a in args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = args.index(a)
                argumentos[cortado[1]] = args[posicao_e + 1]
            else:
                argumentos[a] = 1
        return argumentos

    def set_acao(self):
        if 'a' in self.__argumentos:
            func = getattr(Disparos, '{}'.format(self.__argumentos['a']))
            func(self)

