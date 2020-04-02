import pytest

from app.uteis import Uteis
from app.exception import KeysInvalido


def test_deve_retornar_o_endereco_programacao_quando_tem_arg_programacao():
    util = Uteis(['programacao'])
    endereco = '/home/www/json/keys.json'
    assert util.endereco == endereco

def test_deve_retornar_o_endereco_localhost_quando_tem_arg_localhost():
    util = Uteis(['localhost'])
    endereco = '/var/www/json/keys.json'
    assert util.endereco == endereco

def test_deve_retornar_o_uri_local_quando_tem_arg_programacao():
    util = Uteis(['programacao'])
    uri = 'http://localhost:5000/'
    assert util.uri == uri

def test_deve_retornar_o_endereco_localhost_quando_sem_arg():
    util = Uteis([])
    uri = 'http://imoveis.powempresas.com/'
    assert util.uri == uri

def test_deve_existir_user_em_keys_quando_localhost():
    util = Uteis(['localhost'])
    util.set_keys()
    assert len(util.keys)

def test_nao_deve_ter_keys_quando_programacao():
    util = Uteis(['programacao'])
    with pytest.raises(KeysInvalido):
        util.set_keys()
