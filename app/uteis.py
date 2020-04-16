from app.exception import KeysInvalido
import json

class Uteis:

    def __init__(self, args):
        self.__args = args
        self.set_endereco_keys()
        self.set_uri()
        self.set_cwd()
        self.__keys = {}
        self.set_teste()

    def set_uri(self):
        if self._is_localhost() or self._is_programacao():
            self.__uri = 'http://localhost:5000/'
            self.__localhost = True
        else:
            self.__uri = 'http://imoveis.powempresas.com/'
            self.__localhost = False

    def set_endereco_keys(self):
        if self._is_programacao():
            self.__endereco = '/home/www/json/keys.json'
        else:
            self.__endereco = '/var/www/json/keys.json'

    def set_keys(self):
        try:
            with open(self.endereco) as json_file:
                keys = json.load(json_file)
                self.__keys = keys['basic']
                self.__keysEmail = keys['email']['iagente']
        except:
             raise KeysInvalido('Não existem estas chaves')

    def set_teste(self):
        self.__teste = 'teste' in self.__args

    def _is_localhost(self):
        return 'localhost' in self.__args

    def _is_programacao(self):
        return 'programacao' in self.__args

    @property
    def teste(self):
        return self.__teste

    @property
    def cwd(self):
        return self.__cwd

    @property
    def uri(self):
        return self.__uri

    @property
    def localhost(self):
        return self.__localhost

    @property
    def keys(self):
        return self.__keys

    @property
    def keysEmail(self):
        return self.__keysEmail

    @property
    def endereco(self):
        return self.__endereco

    def set_cwd(self):
        self.__cwd = '/var/www/python/emailMkt/app'


