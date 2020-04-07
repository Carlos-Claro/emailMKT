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

from email_validator import validate_email, EmailNotValidError

from app.exception import ContatosInvalido, ImoveisInvalido, EmailInvalido
from app.logs import Logs
from app.uteis import Uteis
from app.request import Request


class Disparos:

    def __init__(self, args):
        self.__inicio = time.time()
        self.__args = args
        self.__uteis = Uteis(args)
        self.__cidades = Cidades(args)
        self._set_totais(0)

    @property
    def args(self):
        return self.__args

    def set(self):
        contatos = Contatos(self.args)
        if contatos.set_contatos():
            for contato in contatos.itens:
                print(contato)
                if self.__cidades.set_cidades(contato['id']):
                    try:
                        contato_email = Contato(self.args, contato, self.__cidades.get_itens(contato['id'])).set()
                        self.__totais['ok'] += 1
                    except:
                        self.__totais['error'] += 1
                else:
                    self.__totais['error'] += 1


    def _set_totais(self,qtde):
        self.__totais = {
            'total': qtde,
            'ok': 0,
            'error': 0
        }

    @property
    def totais(self):
        return self.__totais

class Contato:
    def __init__(self,args,contato,cidades):
        self.__cidades = cidades
        self.__contato = contato
        self.__args = args

    @property
    def contato(self):
        return self.__contato

    @property
    def imoveis(self):
        return self.__imoveis

    def set(self):
        try:
            v = validate_email(self.contato['email'])
            self.__imoveis = Imoveis(self.__args, self.__contato)
        except EmailNotValidError as e:
            message = '{} - Email inválido: {} - id {}'.format(str(e), self.contato['email'], self.contato['id'])
            self.log_error(message)
            raise EmailInvalido(message)
        except ImoveisInvalido:
            return False



    def log_error(self, message):
        data = {
            'formato': 'contato_erro',
            'arquivo': 'erro',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message':message
            }
        }
        Logs(data)




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

    def get_itens(self,ids):
        ids_ = tuple(map(int, ids.split(',')))
        retorno = {'itens':{},'principal':0}
        c = 0
        for id in ids_:
            if c == 0:
                retorno['principal'] = id
            retorno['itens'][id] = self.itens[id]
            c += 1
        return retorno

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
    def __init__(self, args, contato):
        self.__args = args
        self.__uteis = Uteis(self.__args)
        self.__contato = contato
        self._set_imoveis()

    @property
    def itens(self):
        return self.__imoveis

    @property
    def contato(self):
        return self.__contato

    def _set_filtro(self):
        data = {}
        data['limit'] = 6
        data['tipo'] = self.contato['tipo_negocio_item']
        data['id_tipo'] = self.contato['id_tipo_item']
        data['cidades_id'] = self.contato['cidades']
        return data

    def _set_imoveis(self):
        data = {'filtro': self._set_filtro()}
        data['url_tipo'] = 'imoveis'
        data['tipo'] = 'get'
        self.__imoveis = Request(self.__uteis).request(data)
        print(self.__imoveis)
        if not len(self.__imoveis['itens']['itens']):
            message = 'Nenhum imovel para este contato id_contato: {}'.format(self.contato['id'])
            self.log_error(message)
            raise ImoveisInvalido(message)


    def log_error(self, message):
        data = {
            'formato': 'imoveis_erro',
            'arquivo': 'erro',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message':message
            }
        }
        Logs(data)

class Email:
    def __init__(self):
        pass


if __name__ == '__main__':
    Disparos()
