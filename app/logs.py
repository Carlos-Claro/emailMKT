import datetime

from app.exception import LogInvalido


class Logs:

    def __init__(self, data):
        formato = self.formatos({'tipo':'formato', 'chave':data['formato']})
        arquivo = self.formatos({'tipo':'arquivo', 'chave':data['arquivo']})
        linha = self.formata(formato, data['data'])
        self.set_log(arquivo, linha)

    def formatos(self, data):
        arquivos = {
            'log': '/var/log/sistema/email_mkt.log',
            'erro': '/var/log/sistema/error_email_mkt.log'
        }
        formatos = {
            'request' : '{data} - status_code {status_code} - funcao: {tipo} - qtde: {qtde} - tempo: {tempo} ',
            'request_erro': '{data} - status_code {status_code} - message {message} - erro_request ',
            'contatos_erro': '{data} - message {message} - erro_contatos ',
            'disparos': '{data} - status_code {status_code} - qtde: {qtde} - funcao: disparos_totais - tempo: {tempo} ',
            'email' : '{data} - status_code {status_code} - id_cadastro: {id_cadastro} - imoveis: {imoveis} - funcao: email_individual - tempo: {tempo} ',
            'log_erro': '{data} - message {message} - erro_log ',
            'cidades_erro': '{data} - message {message} - erro_cidades ',
        }
        if data['tipo'] == 'arquivo':
            try:
                return arquivos[data['chave']]
            except KeyError:
                message = 'Não existe este arquivo - {}'.format(data['chave'])
                self.log_error(message)
                raise LogInvalido(message)
        try:
            return formatos[data['chave']]
        except KeyError:
            message = 'Não existe este formato - {}'.format(data['chave'])
            self.log_error(message)
            raise LogInvalido(message)

    def set_log(self,arquivo,linha):
        try:
            with open(arquivo, 'a') as arq:
                arq.write(linha)
                arq.write('\r\n')
            return True
        except:
            message = 'não foi possivel adicionar a linha, verifique as permissões do arquivo.'
            self.log_error(message)
            raise LogInvalido(message)

    def formata(self, chave, valor):
        return chave.format(**valor)

    def log_error(self, message):
        data = {
            'formato': 'log_erro',
            'arquivo': 'erro',
            'data': {
                'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': message
            }
        }
        Logs(data)


