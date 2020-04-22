import pytest
import datetime

from app.exception import LogInvalido
from app.logs import Logs


@pytest.fixture
def log_request():
    return {
        'formato': 'request',
        'arquivo':'log',
        'data': {
            'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'qtde': 1,
            'tempo': 2,
            'status_code': 100,
            'tipo': 'contatos'
        }
    }

@pytest.fixture
def log_request_invalido():
    return {
        'formato': 'request___',
        'arquivo':'log',
        'data': {
            'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'qtde': 1,
            'tempo': 2,
            'status_code': 100,
            'tipo': 'contatos'
        }
    }

@pytest.fixture
def log_arquivo_invalido():
    return {
        'formato': 'request',
        'arquivo':'log____',
        'data': {
            'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'qtde': 1,
            'tempo': 2,
            'status_code': 100,
            'tipo': 'contatos'
        }
    }


def test_deve_inserir_e_formatar_data_e_inserir_no_arquivo(log_request):
    assert Logs(log_request)


def test_deve_gerar_exception_quando_formato_invalido(log_request_invalido):
    with pytest.raises(LogInvalido):
        Logs(log_request_invalido)

def test_deve_gerar_exception_quando_arquivo_invalido(log_arquivo_invalido):
    with pytest.raises(LogInvalido):
        Logs(log_arquivo_invalido)

