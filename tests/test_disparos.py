import pytest

from app.disparos import Disparos, Contatos
from app.exception import ContatosInvalido


@pytest.fixture
def args_dias_1():
    args = {}
    args['localhost'] = 1
    args['dias'] = 1
    return args

@pytest.fixture
def args_dias_30():
    args = {}
    args['localhost'] = 1
    args['dias'] = 30
    return args


def test_deve_conter_contatos_quando_dias_igual_a_30(args_dias_30):
    assert Contatos(args_dias_30).set_contatos()

def test_nao_deve_conter_contatos_quando_dias_igual_a_1(args_dias_1):
    with pytest.raises(ContatosInvalido):
        Contatos(args_dias_1).set_contatos()
