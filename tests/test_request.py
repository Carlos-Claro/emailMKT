from app.exception import KeysInvalido, RequestInvalido
from app.request import Request
import pytest

from app.uteis import Uteis


@pytest.fixture
def uteis_localhost():
    return Uteis(['localhost'])

@pytest.fixture
def uteis_programacao():
    return Uteis(['programacao'])

@pytest.fixture
def uteis_():
    return Uteis([])

@pytest.fixture
def data_contatos():
    data = {'filtro': {}}
    data['filtro']['limit'] = 5
    data['filtro']['dias'] = 60
    data['url_tipo'] = 'contatos'
    data['tipo'] = 'get'
    return data

@pytest.fixture
def data_contatos_tipo_errado():
    data = {'filtro': {}}
    data['filtro']['limit'] = 5
    data['filtro']['dias'] = 60
    data['url_tipo'] = 'contatos_errado'
    data['tipo'] = 'get'
    return data


def test_deve_retornar_url_localhost_quando_uteis_localhost(uteis_localhost):
    request = Request(uteis_localhost)
    uri = 'http://localhost:5000/'
    assert request.uri == uri

def test_deve_retornar_url_quente_quando_uteis_(uteis_):
    request = Request(uteis_)
    uri = 'http://imoveis.powempresas.com/'
    assert request.uri == uri

def test_deve_retornar_url_contatos_quando_get_tipo_contatos(uteis_localhost):
    request = Request(uteis_localhost)
    uri = 'http://localhost:5000/get_contatos/'
    assert request.get_tipo('contatos') == uri

def test_deve_retornar_url_false_quando_get_tipo_invalido(uteis_localhost):
    request = Request(uteis_localhost)
    assert not request.get_tipo('')

def test_deve_retornar_url_imoveismongo_quando_get_tipo_imoveis(uteis_localhost):
    request = Request(uteis_localhost)
    uri = 'http://localhost:5000/imoveismongo/'
    assert request.get_tipo('imoveis') == uri

def test_deve_retornar_auth_object_quando_localhost(uteis_localhost):
    request = Request(uteis_localhost)
    request.set_auth()
    assert request.auth

def test_nao_deve_ter_keys_quando_programacao(uteis_programacao):
    request = Request(uteis_programacao)
    with pytest.raises(KeysInvalido):
        request.set_auth()

def test_deve_retornar_contatos_quando_request_com_data(uteis_localhost, data_contatos):
    request = Request(uteis_localhost)
    contatos = request.request(data_contatos)
    assert len(contatos)

def test_request_error(uteis_localhost, data_contatos_tipo_errado):
    request = Request(uteis_localhost)
    with pytest.raises(RequestInvalido):
        print(request.request(data_contatos_tipo_errado))

