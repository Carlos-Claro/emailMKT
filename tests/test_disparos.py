import pytest

from app.disparos import Contatos, Cidades, Imoveis, Contato
from app.exception import ContatosInvalido, ImoveisInvalido, EmailInvalido


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

@pytest.fixture
def contato():
    return {
        'cidade': '',
        'cidades': '1',
        'data': '09/03/2020 19:42',
        'email': 'programacao@pow.com.br',
        'id': '575933',
        'id_cadastro': 143364,
        'id_itens': '2023787',
        'id_tipo_item': '10',
        'nome': 'Teste Desenvolvimento',
        'qtde_contatos': 1,
        'tabela': 'imoveis',
        'tipo_negocio_item': 'venda',
        'tipos_item': 'sobrado'
    }

@pytest.fixture
def contato_invalido():
    return {
        'cidade': '',
        'cidades': '2',
        'data': '09/03/2020 19:42',
        'email': 'programacao@pow.com.br',
        'id': '575933',
        'id_cadastro': 143364,
        'id_itens': '2023787',
        'id_tipo_item': '155',
        'nome': 'Teste Desenvolvimento',
        'qtde_contatos': 1,
        'tabela': 'imoveis',
        'tipo_negocio_item': 'venda',
        'tipos_item': 'sobrado'
    }

@pytest.fixture
def contato_invalido_email():
    return {
        'cidade': '',
        'cidades': '2',
        'data': '09/03/2020 19:42',
        'email': 'programacao@po.co.br',
        'id': '575933',
        'id_cadastro': 143364,
        'id_itens': '2023787',
        'id_tipo_item': '155',
        'nome': 'Teste Desenvolvimento',
        'qtde_contatos': 1,
        'tabela': 'imoveis',
        'tipo_negocio_item': 'venda',
        'tipos_item': 'sobrado'
    }

@pytest.fixture
def contato_dois_tipos():
    return {
        'cidade': '',
        'cidades': '1',
        'data': '09/03/2020 19:42',
        'email': 'programacao@pow.com.br',
        'id': '575933',
        'id_cadastro': 143364,
        'id_itens': '2023787',
        'id_tipo_item': '10,1',
        'nome': 'Teste Desenvolvimento',
        'qtde_contatos': 2,
        'tabela': 'imoveis',
        'tipo_negocio_item': 'venda',
        'tipos_item': 'sobrado,apartamento'
    }

@pytest.fixture
def contato_dois_tipos():
    data = {}
    data['limit'] = 6
    data['imovel_para'] = 'venda'
    data['tem_foto'] = True
    data['id_tipo'] = '1,2'
    data['cidades_id'] = '1,2'
    return filtro

@pytest.fixture
def contato_um_tipo():
    data = {}
    data['limit'] = 6
    data['imovel_para'] = 'venda'
    data['tem_foto'] = True
    data['id_tipo'] = '2'
    data['cidades_id'] = '2'
    return filtro

@pytest.fixture
def contato_false():
    filtro = {}
    return filtro

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


def test_deve_retornar_cidade_quando_enviado_uma_cidade_valida(args_dias_30):
    cidades = Cidades(args_dias_30)
    cidades.set_cidades('2,1')
    c = cidades.get_itens('1,2')
    assert c['itens'][2]['link'] == 'curitiba_pr'

def test_deve_retornar_cidade_quando_enviado_uma_cidade_valida_sjp(args_dias_30):
    cidades = Cidades(args_dias_30)
    ids = '2,1'
    cidades.set_cidades(ids)
    c = cidades.get_itens('1,2')
    assert c['itens'][c['principal']]['link'] == 'sao_jose_dos_pinhais_pr'

def test_deve_retornar_seis_imoveis_quando_contato_valido(args_dias_30,contato):
    imoveis = Imoveis(args_dias_30,contato)
    assert imoveis.itens['itens']['qtde'] == 6

def test_nao_deve_retornar_imoveis_quando_contato_invalido(args_dias_30,contato_invalido):
    with pytest.raises(ImoveisInvalido):
        Imoveis(args_dias_30,contato_invalido)

def test_deve_retornar_raises_email_quando_contato_invalido(args_dias_30,contato_invalido_email):
    with pytest.raises(EmailInvalido):
        cidades = Cidades(args_dias_30)
        cidades.set_cidades(contato_invalido_email['cidades'])
        contato = Contato(args_dias_30, contato_invalido_email, cidades).set()


def test_deve_retornar_raises_quando_contato_valido_via_contato(args_dias_30,contato_invalido):
    cidades = Cidades(args_dias_30)
    cidades.set_cidades(contato_invalido['cidades'])
    contato = Contato(args_dias_30, contato_invalido, cidades).set()
    assert not contato

def test_deve_retornar_seis_imoveis_quando_contato_valido(args_dias_30,contato):
    imoveis = Imoveis(args_dias_30,contato)
    assert imoveis.itens['itens']['qtde'] == 6
