#############################################
# ############## POW INTERNET ############# #
# Disparo de ofertas para usuarios          #
# cadastrados nos ultimos 60 dias           #
# Acessa RESTAPIImoveis                     #
# Data 11.03.2020                           #
# Uso,                                      #
# tags: localhost, BasicAuth, keys, json    #
# -verbose (debuga os passos e o tempo)     #
# -tempo (apresenta o tempo)                #
# Relatorios: /var/log/sistema/email_mkt.log #
#
#
###########################################

# -*- coding: utf-8 -*-

import datetime
import time
import os
import sys
import json
import random

from app.exception import ContatosInvalido
from app.logs import Logs
from app.uteis import Uteis
from app.request import Request


class Disparos:

    def __init__(self, args):
        self.__inicio = time.time()
        self.__args = args
        self.__uteis = Uteis(args)
        self.__cidades = Cidades(args)

    @property
    def args(self):
        return self.__args

    def set(self):
        contatos = Contatos(self.args)
        if contatos.set_contatos():
            self._set_totais()
            for contato in contatos.itens:
                self.processa_item(contato)

    def processa_item(self,contato):
        self.__cidades.set_cidades(contato['ids'])
        imoveis = Imoveis(self.__args, contato, self.__cidades)




    def get_message(self, contato):
        data = {}
        if contato['id_cidade'] in self.cidades:
            data['cidade'] = ''
        print(contato)
        return True

    def _set_totais(self,qtde):
        self.__totais = {
            'total': qtde,
            'ok': 0,
            'error': 0
        }

    @property
    def totais(self):
        return self.__totais


class Contatos:
    def __init__(self, args):
        self.__args = args
        self.__uteis = Uteis(args)

    def set_contatos(self):
        data = self._get_filtro()
        data['url_tipo'] = 'contatos'
        data['tipo'] = 'get'
        self.__contatos = Request(self.__uteis).request(data)
        if self.itens:
            return True
        else:
            message = 'Nenhum contato retornado'
            self.log_error(message)
            raise ContatosInvalido(message)

    def _get_filtro(self):
        data = {'filtro': {}}
        data['filtro']['limit'] = 10
        data['filtro']['dias'] = 60
        print('dias' in self.__args)
        if 'qtde' in self.__args:
            data['filtro']['limit'] = self.__args['qtde']
        if 'dias' in self.__args:
            data['filtro']['dias'] = self.__args['dias']
        return data

    @property
    def itens(self):
        return self.__contatos

    def log_error(self, message):
        data = {
            'formato': 'contatos_erro',
            'arquivo': 'erro',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message':message
            }
        }
        Logs(data)

class Cidades:
    def __init__(self, args):
        self.__args = args
        self.__uteis = Uteis(args)
        self.__cidades = {}

    @property
    def itens(self):
        return self.__cidades

    def set_cidades(self,ids):
        ids_ = tuple(map(int, ids.split(',')))
        if ids_[0] in self.itens:
            return True
        return self.get_cidades(ids)


    def get_cidades(self,ids):
        data = {'filtro': {}}
        data['filtro']['ids'] = ids
        data['url_tipo'] = 'cidades_in'
        data['tipo'] = 'get'
        cidades = Request(self.__uteis).request(data)
        if len(cidades):
            for cidade in cidades:
                self.__cidades[cidade['id']] = {
                    'logo': cidade['topo'],
                    'titulo':cidade['nome'],
                    'link':cidade['link'],
                    'portal':cidade['portal']
                }
            if len(cidades) != len(ids.split(',')):
                message = 'Uma ou mais cidades não encontradas com os ids: {}'.format(ids)
                self.log_error(message)
            return True
        message = 'Nenhuma cidade encontrada com os ids: {}'.format(ids)
        self.log_error(message)
        return False

    def log_error(self, message):
        data = {
            'formato': 'cidades_erro',
            'arquivo': 'erro',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message':message
            }
        }
        Logs(data)

class Imoveis:
    def __init__(self, args, contato, cidades):

        pass

class Email:
    def __init__(self):
        pass


if __name__ == '__main__':
    Disparos()
