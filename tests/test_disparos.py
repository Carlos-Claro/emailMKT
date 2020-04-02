import pytest

from app.disparos import Disparos, Contatos, Cidades
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

def test_deve_retornar_true_quando_enviado_cidade_valida(args_dias_30):
    cidades = Cidades(args_dias_30)
    assert cidades.set_cidades('1')

def test_deve_encontrar_cidade_quando_enviado_cidade_valida(args_dias_30):
    cidades = Cidades(args_dias_30)
    item = cidades.set_cidades('1')
    assert cidades.itens[1]['link'] == 'sao_jose_dos_pinhais_pr'

def test_deve_encontrar_cidade_quando_enviado_cidades_validas(args_dias_30):
    cidades = Cidades(args_dias_30)
    item = cidades.set_cidades('1,2')
    assert cidades.itens[1]['link'] == 'sao_jose_dos_pinhais_pr'

def test_deve_encontrar_cidade_quando_enviado_cidades_validas_cwb(args_dias_30):
    cidades = Cidades(args_dias_30)
    item = cidades.set_cidades('1,2')
    assert cidades.itens[2]['link'] == 'curitiba_pr'

def test_deve_encontrar_cidade_quando_enviado_uma_cidade_valida_e_outra_invalida(args_dias_30):
    cidades = Cidades(args_dias_30)
    assert cidades.set_cidades('1,99999')

def test_deve_encontrar_cidade_quando_enviado_uma_cidade_valida_e_outra_invalida_retornar_cwd(args_dias_30):
    cidades = Cidades(args_dias_30)
    cidades.set_cidades('2,99999')
    assert cidades.itens[2]['link'] == 'curitiba_pr'

def test_nao_deve_encontrar_cidade_quando_enviado_cidade_invalida(args_dias_30):
    cidades = Cidades(args_dias_30)
    assert not cidades.set_cidades('989898')

