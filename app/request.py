import datetime
import sys
import time

import requests
from requests.auth import HTTPBasicAuth

from app.exception import KeysInvalido, RequestInvalido
from app.logs import Logs
from app.uteis import Uteis


class Request:

    def __init__(self, uteis: Uteis):
        self.__uteis = uteis
        self.__uri = self.__uteis.uri
        self.__auth = []
        self.__inicio = time.time()

    @property
    def uri(self):
        return self.__uri

    @property
    def auth(self):
        return self.__auth

    def get_tipo(self,tipo):
        itens = {
            'contatos': self.__uri + 'get_contatos/',
            'contatos_errado': self.__uri + 'get_contatos__/',
            'cidades_in': self.__uri + 'get_cidade_in_ids/',
            'imoveis': self.__uri + 'imoveismongo/'
        }
        if tipo in itens:
            try:
                return itens[tipo]
            except KeyError:
                message = 'Nenhuma chave disponivel'
                self.log_error(100, message)
                raise RequestInvalido(message)
        return False

    def set_auth(self):
        try:
            self.__uteis.set_keys()
        except:
            raise KeysInvalido('Não foi possivel setar key')
        user = self.__uteis.keys['user']
        passwd = self.__uteis.keys['passwd']
        self.__auth = HTTPBasicAuth(user, passwd)

    def set_data_log_inicial(self,url_tipo):
        self.__data_log = {'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           'qtde': 0,
                           'tempo': 0,
                           'status_code': 100,
                           'tipo': url_tipo
                           }

    def set_data_log(self,campo,valor):
        self.__data_log[campo] = valor

    @property
    def data_log(self):
        return self.__data_log

    def request(self,data):
        self.set_auth()
        self.set_data_log_inicial(data['url_tipo'])
        url = self.get_tipo(data['url_tipo'])
        try:
            if data['tipo'] == 'get':
                itens = requests.get(url, params=data['filtro'], auth=self.auth)
            elif data['tipo'] == 'post':
                itens = requests.post(url, params=data['itens'], auth=self.auth)
            status_code = itens.status_code
        except requests.exceptions.HTTPError as errh:
            status_code = 403
            self.log_error(status_code,errh)
            raise RequestInvalido(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            status_code = 401
            self.log_error(status_code, errc)
            raise RequestInvalido(errc)
        except requests.exceptions.Timeout as errt:
            status_code = 408
            self.log_error(status_code, errt)
            raise RequestInvalido(errt)
        except requests.exceptions.RequestException as err:
            status_code = 400
            self.log_error(status_code, err)
            raise RequestInvalido(err)
        except:
            status_code = 500
            message = 'Nenhuma conexão válida {}'.format(url)
            self.log_error(status_code, message)
            raise RequestInvalido(message)
        self.set_data_log('status_code',status_code)
        i = {}
        print(status_code)
        if 200 <= status_code <= 299:
            i = itens.json()
            self.set_data_log('qtde', len(i))
        else:
            message = 'Problemas na conexão, {} {}'.format(data['url_tipo'], url)
            self.log_error(status_code, message)
            raise RequestInvalido(message)
        fim = time.time()
        self.set_data_log('tempo', fim - self.__inicio)
        log = {
            'formato': 'request',
            'arquivo':'log',
            'data': self.data_log
        }
        Logs(log)
        return i

    def log_error(self, codigo, message):
        data = {
            'formato': 'request_erro',
            'arquivo': 'erro',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status_code':codigo,
                'message':message
            }
        }
        Logs(data)
