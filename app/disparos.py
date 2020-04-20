#############################################
# ############## POW INTERNET ############# #
# Disparo de ofertas para usuarios          #
# cadastrados nos ultimos 60 dias           #
# Acessa RESTAPIImoveis                     #
# Data 11.03.2020 - Op: 17.04.2020          #
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
import smtplib
from email.message import EmailMessage


from app.exception import ContatosInvalido, ImoveisInvalido, EmailInvalido, CorpoInvalido
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
            self.contatos(contatos.itens)
        fim = time.time()
        self.log(fim-self.__inicio)

    def contatos(self,contatos):
        self._set_totais(len(contatos))
        for contato in contatos:
            tem_cidade = self.__cidades.set_cidades(contato['cidades'])
            if tem_cidade:
                try:
                    contato_ = Contato(self.args, contato, self.__cidades.get_itens(contato['cidades'])).set()
                    if contato_:
                        self.__totais['ok'] += 1
                    else:
                        self.__totais['error'] += 1
                except:
                    self.__totais['error'] += 1
            else:
                self.__totais['error'] += 1


    def log(self,tempo):
        data = {
            'formato': 'disparos',
            'arquivo': 'log',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total':self.__totais['total'],
                'ok':self.__totais['ok'],
                'error':self.__totais['error'],
                'tempo':tempo
            }
        }
        Logs(data)

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
        self.__uteis = Uteis(self.__args)
        self.__uteis.set_keys()

    @property
    def contato(self):
        return self.__contato

    def set(self):
        inicio = time.time()
        try:
            v = validate_email(self.contato['email'])
            imoveis = Imoveis(self.__args, self.__contato)
            corpo = Corpo_email(self.__cidades,self.__contato, imoveis.itens['itens'], self.__uteis)
            c = corpo.get_imoveis_corpo()
            if self._envio(c):
                #upload
                fim = time.time()
                self.log('ok',fim-inicio)
                self.update_contato(self.contato['id'])
                return True
            fim = time.time()
            self.log('erro_disparo',fim-inicio)
            self.update_contato(self.contato['id'])
            return False
        except EmailNotValidError as e:
            message = '{} - Email inválido: {} - id {}'.format(str(e), self.contato['email'], self.contato['id'])
            self.log_error(message)
            self.update_contato(self.contato['id'])
            raise EmailInvalido(message)
        except ImoveisInvalido:
            message = 'Imoveis invalidos: id {}'.format(self.contato['id'])
            self.log_error(message)
            self.update_contato(self.contato['id'])
            return False
        except Exception as a:
            message = '{} id {}'.format(a,self.contato['id'])
            self.log_error(message)
            self.update_contato(self.contato['id'])
            return False

    def _titulo_email(self):
        itens = [
            'Encontre seu novo imóvel',
            'Mais ofertas de imóvel',
            'Encontre mais imóveis hoje mesmo',
            'Continue buscando mais imóveis',
            'Temos mais imóveis para você'
        ]
        index = random.randint(0, len(itens) - 1)
        return itens[index]

    def _envio(self,corpo):
        try:
            msg = EmailMessage()
            msg['Subject'] = self._titulo_email()
            msg['From'] = 'envio@powinternet.com.br'
            if self.__uteis.teste:
                msg['To'] = 'carlosclaro79@gmail.com'
            else:
                msg['To'] = self.contato['email']
            msg.add_header('Content-Type', 'text/html')
            msg.set_content(corpo, subtype='html')
            s = smtplib.SMTP(self.__uteis.keysEmail['smtp_host'], int(self.__uteis.keysEmail['smtp_port']))
            s.login(self.__uteis.keysEmail['smtp_user'], self.__uteis.keysEmail['smtp_pass'])
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()
            return True
        except Exception as a:
            message = '{} id {}'.format(a, self.contato['id'])
            self.log_error(message)
            return False

    def update_contato(self, id):
        data = {'itens':{}}
        data['itens']['ids'] = id
        data['url_tipo'] = 'contato_up'
        data['tipo'] = 'put'
        return Request(self.__uteis).request(data)


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

    def log(self,status,tempo):
        data = {
            'formato': 'disparo',
            'arquivo': 'log',
            'data':{
                'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'id':self.contato['id'],
                'email': self.contato['email'],
                'tempo': tempo,
                'status': status
            }
        }
        Logs(data)



class Corpo_email:
    def __init__(self, cidades, contato, imoveis, uteis):
        self.__contato = contato
        self.__cidades = cidades
        self.__imoveis = imoveis
        self.__uteis = uteis
        self._imovel_html()
        self._link_html()
        self._corpo_html()
        self._css_html()


    def _corpo_html(self):
        with open('{}/views/corpo.html'.format(self.__uteis.cwd),'r') as a:
            self.html_corpo = a.read()

    def _css_html(self):
        with open('{}/views/bootstrap.css'.format(self.__uteis.cwd),'r') as a:
            self.html_css = a.read()

    def _link_html(self):
        with open('{}/views/link.html'.format(self.__uteis.cwd),'r') as a:
            self.html_link = a.read()

    def _imovel_html(self):
        with open('{}/views/imovel.html'.format(self.__uteis.cwd),'r') as a:
            self.html_imovel = a.read()

    def _set_imoveis_corpo(self):
        imoveis = []
        for imovel in self.__imoveis['itens']:
            campos = self._set_campos(imovel)
            self._set_html_imovel(campos)
            imoveis.append(self.html_imovel.format(**campos))
        retorno = '<tr>'
        x = 0
        for i in imoveis:
            retorno += '<td>{}</td>'.format(i)
            x += 1
            if x%2 == 0:
                retorno += '</tr><tr>'
        retorno += '</tr>'
        return retorno

    def get_imoveis_corpo(self):
        try:
            corpo_imoveis = self._set_imoveis_corpo()
            email = self._set_html_corpo(corpo_imoveis)
            return email
        except Exception as b:
            message = 'Erro compondo imoveis html {}'.format(b)
            self.log_error(message)
            raise CorpoInvalido(message)

    def _set_html_imovel(self,campos):
        try:
            a = self.html_imovel.format(**campos)
            return a
        except Exception as b:
            message = 'Problema no html do contato {}'.format(b)
            self.log_error(message)
            raise ContatoInvalido(message)

    def _set_link(self,imovel):
        return '{}/imovel/{tipo_negocio}-{imoveis_tipos_link}' \
               '-{cidades_link}-{bairros_link}-{imobiliaria_nome_seo}' \
               '/{id}/e'.format(self.__cidades['itens'][self.__cidades['principal']]['portal'],**imovel)

    def _set_titulo(self,imovel):
        return '{} {}, {}'.format(imovel['imoveis_tipos_titulo'],self._set_tipo_negocio(imovel['tipo_negocio']), imovel['bairro'])

    def _set_tipo_negocio(self,tipo):
        if tipo == 'venda':
            return ' à Venda'
        return ' para Alugar '


    def _set_campos(self,imovel):
        retorno = {
            'classe': imovel['tipo_negocio'],
            'imovel_link': self._set_link(imovel),
            'imovel_titulo': self._set_titulo(imovel),
            'image_principal': self._set_image_principal(imovel['images']),
            'image_descricao' : self._set_titulo_image(imovel),
            'imoveis_tipos_titulo': imovel['imoveis_tipos_titulo'],
            'bairro_titulo': imovel['bairro'],
            'cidade_titulo': imovel['cidade_nome'],
            'relacionado_link': self._set_link_relacionado(imovel),
            'relacionado_titulo': self._set_titulo_relacionado(imovel)
        }
        return retorno

    def _set_image_principal(self, images):
        return images[0]['arquivo']

    def _set_titulo_image(self, imovel):
        if len(imovel['images'][0]['titulo']):
            return imovel['images'][0]['titulo']
        return self._set_titulo(imovel)

    def _set_link_relacionado(self, imovel):
        return '{}/{imoveis_tipos_link}-{tipo_negocio}-{cidades_link}-{bairros_link}/'.format(
            self.__cidades['itens'][self.__cidades['principal']]['portal'], **imovel)

    def _set_titulo_relacionado(self, imovel):
        return '{} {}, {}'.format(imovel['imoveis_tipos_titulo'], self._set_tipo_negocio(imovel['tipo_negocio']),
                                  imovel['bairro'])


    def _set_html_corpo(self, corpo_imoveis):
        try:
            campos = self._set_campo_corpo(corpo_imoveis)
            b = self.html_corpo.format(**campos)
            return b
        except Exception as a:
            message = 'Erro compondo corpo html {}'.format(a)
            self.log_error(message)
            raise CorpoInvalido(message)

    def _set_campo_corpo(self, imoveis):
        a = {
            'titulo': 'Encontre seu novo Imóvel',
            'portal_link': self.__cidades['itens'][self.__cidades['principal']]['portal'],
            'portal_logo': 'https://admin.powempresas.com/portais/logos/{}'.format(self.__cidades['itens'][self.__cidades['principal']]['logo']),
            'portal_titulo': 'Imóveis em {}'.format(self.__cidades['itens'][self.__cidades['principal']]['titulo']),
            'assunto': 'Encontre seu novo Imóvel em {} no portal {}'.format(self.__cidades['itens'][self.__cidades['principal']]['titulo'], self.__cidades['itens'][self.__cidades['principal']]['portal']),
            'imoveis': imoveis,
            'contato_tipo': self.__contato['tipo_negocio_item'],
            'cidade_titulo': self.__cidades['itens'][self.__cidades['principal']]['titulo'],
            'tipos_links': self._set_tipos_links(),
            'contato_nome': self.__contato['nome'],
            'contato_email': self.__contato['email'],
            'css': self.html_css
        }
        return a

    def _set_tipo_negocio_int(self):
        data = {
            'venda':0,
            'locacao':1
        }
        return data[self.__contato['tipo_negocio_item']]

    def _set_tipos_links(self):
        menu = self.__cidades['itens'][self.__cidades['principal']]['menu'][self._set_tipo_negocio_int()]
        links = []
        for item in menu['itens']:
            campos = {
                'tipo_link': '{}/{}-{}-{}'.format(self.__cidades['itens'][self.__cidades['principal']]['portal'],
                                                   item['link'],
                                                   menu['link'],
                                                   self.__cidades['itens'][self.__cidades['principal']]['link']
                                                   ),
                'titulo_link': '{} {} em {}'.format(menu['titulo'],item['descricao'], self.__cidades['itens'][self.__cidades['principal']]['titulo']),
                'titulo': '{} <br> + {} Imóveis'.format(item['descricao'],item['qtde'])
            }
            links.append(self.html_link.format(**campos))
        return ''.join(links)

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
        data['filtro']['limit'] = 1
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
                    'portal':cidade['portal'],
                    'menu':cidade['menu']
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
        print(data)
        self.__imoveis = Request(self.__uteis).request(data)
        print(self.__imoveis)
        if not len(self.__imoveis['itens']['itens']):
            message = 'Nenhum imovel para este id_contato: {}'.format(self.contato['id'])
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
