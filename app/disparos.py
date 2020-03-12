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

import requests
import datetime
import time
import os
import sys
import json
import random
from requests.auth import HTTPBasicAuth


class Disparos(object):

    def __init__(self):
        self.inicio = time.time()
        self.args = sys.argv
        endereco = '/var/www/json/keys.json'
        if 'localhost' in self.args:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        elif 'programacao' in self.args:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
            endereco = '/home/www/json/keys.json'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
        with open(endereco) as json_file:
            data = json.load(json_file)
        self.user = data['basic']['user']
        self.passwd = data['basic']['passwd']
        self.auth = HTTPBasicAuth(self.user, self.passwd)
        self.URL_GET_CONTATOS = self.URI + 'get_contatos/'
        self.URL_POST_CIDADES = self.URI + 'get_cidade_in_ids/'
        self.URL_GET_MONGO = self.URI + 'imoveismongo/'
        self.URL_POST = self.URI + 'imoveis_integra/'
        self.URL_PUT = self.URI + 'imovel/'
        self.ARQUIVO_LOG = '/var/log/sistema/email_mkt.log'
        self.FORMATO_LOG_CONTATOS = '{data} - status_code {status_code} - funcao: get_contatos - tempo: {tempo} '
        self.FORMATO_LOG_DISPAROS = '{data} - status_code {status_code} - qtde: {qtde} - funcao: disparos_totais - tempo: {tempo} '
        self.FORMATO_LOG_EMAIL = '{data} - status_code {status_code} - id_cadastro: {id_cadastro} - imoveis: {imoveis} - funcao: email_individual - tempo: {tempo} '
        self.argumentos = {}
        for a in self.args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = self.args.index(a)
                self.argumentos[cortado[1]] = self.args[posicao_e + 1]
        self.set_acao()


    def set_acao(self):
        if 'python -m unittest' not in self.args:
            if 'a' in self.argumentos:
                func = getattr(Disparos, '{}'.format(self.argumentos['a']))
                func(self)
            else:
                self.set()

    def set(self):
        g = {}
        g['limit'] = 10
        g['dias'] = 60
        if 'qtde' in self.argumentos:
            g['limit'] = self.argumentos['qtde']
        if 'dias' in self.argumentos:
            g['dias'] = self.argumentos['dias']
        data_log_contatos = {'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              'qtde': 0,
                              'tempo': 0,
                             'status_code': 100
                             }
        try:
            itens = requests.get(self.URL_GET_CONTATOS, params=g, auth=self.auth)
            status_code = itens.status_code
        except requests.exceptions.HTTPError as errh:
            status_code = 403
            if 'verbose' in self.argumentos:
                print("Http Error:", errh)
            pass
        except requests.exceptions.ConnectionError as errc:
            status_code = 401
            if 'verbose' in self.argumentos:
                print("Error Connecting:", errc)
            pass
        except requests.exceptions.Timeout as errt:
            status_code = 408
            if 'verbose' in self.argumentos:
                print("Timeout Error:", errt)
            pass
        except requests.exceptions.RequestException as err:
            status_code = 400
            if 'verbose' in self.argumentos:
                print("OOps: Something Else", err)
            pass
        except:
            status_code = 500
            print("OOps: Something Else")
            pass
        data_log_contatos['status_code'] = status_code
        if status_code == 200:
            i = itens.json()
            data_log_contatos['qtde'] = len(i)
            if len(i) > 0:
                self.processa_itens(i)
        self.fim = time.time()
        data_log_contatos['tempo'] = self.fim - self.inicio
        linha = self.FORMATO_LOG_CONTATOS.format(**data_log_contatos)
        with open(self.ARQUIVO_LOG, 'a') as arq:
            arq.write(linha)
            arq.write('\r\n')

    def processa_itens(self,contatos):
        for contato in contatos:
            email = self.get_message(contato)
            print(email)

    cidades = []

    def get_message(self, contato):
        data = {}
        if contato['id_cidade'] in self.cidades:
            data['cidade'] =
        print(contato)
        return True

    def request(self,data):
        try:
            itens = requests.get(self.URL_GET_CONTATOS, params=g, auth=self.auth)
            status_code = itens.status_code
        except requests.exceptions.HTTPError as errh:
            status_code = 403
            if 'verbose' in self.argumentos:
                print("Http Error:", errh)
            pass
        except requests.exceptions.ConnectionError as errc:
            status_code = 401
            if 'verbose' in self.argumentos:
                print("Error Connecting:", errc)
            pass
        except requests.exceptions.Timeout as errt:
            status_code = 408
            if 'verbose' in self.argumentos:
                print("Timeout Error:", errt)
            pass
        except requests.exceptions.RequestException as err:
            status_code = 400
            if 'verbose' in self.argumentos:
                print("OOps: Something Else", err)
            pass
        except:
            status_code = 500
            print("OOps: Something Else")
            pass
        data_log_contatos['status_code'] = status_code
        if status_code == 200:
            i = itens.json()
        return itens

    def set_log(self,data):
        data_log_contatos['tempo'] = self.fim - self.inicio
        linha = self.FORMATO_LOG_CONTATOS.format(**data_log_contatos)
        with open(self.ARQUIVO_LOG, 'a') as arq:
            arq.write(linha)
            arq.write('\r\n')


if __name__ == '__main__':
    Disparos()
