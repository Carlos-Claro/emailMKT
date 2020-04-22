import pytest

from app.disparos import Corpo_email, Imoveis
from app.uteis import Uteis


@pytest.fixture
def inicia():
    contato = {'cidade': '', 'cidades': '1', 'data': '09/03/2020 22:47', 'email': 'julianareis.direito@gmail.com', 'id': '575947', 'id_cadastro': 177912, 'id_itens': '1961673', 'id_tipo_item': '1', 'nome': 'juliana reis', 'qtde_contatos': 1, 'tabela': 'imoveis', 'tipo_negocio_item': 'venda', 'tipos_item': 'apartamento'}
    cidades = {'itens': {1: {'logo': 'tp_imoveissjp.gif', 'titulo': 'São José dos Pinhais', 'link': 'sao_jose_dos_pinhais_pr', 'portal': 'http://www.imoveissaojose.com', 'menu': [{'itens': [{'descricao': 'Andar', 'id': '23', 'link': 'andar', 'qtde': '9'}, {'descricao': 'Apartamento', 'id': '1', 'link': 'apartamento', 'qtde': '1919'}, {'descricao': 'Área', 'id': '4', 'link': 'area', 'qtde': '87'}, {'descricao': 'Barracão / Galpão', 'id': '11', 'link': 'barracao_galpao', 'qtde': '33'}, {'descricao': 'Casa', 'id': '2', 'link': 'casa', 'qtde': '653'}, {'descricao': 'Conjunto Comercial', 'id': '9', 'link': 'conjunto_comercial', 'qtde': '15'}, {'descricao': 'Fazenda', 'id': '6', 'link': 'fazenda', 'qtde': '60'}, {'descricao': 'Hotel', 'id': '17', 'link': 'hotel', 'qtde': '1'}, {'descricao': 'Kitinete', 'id': '12', 'link': 'kitinete', 'qtde': '1'}, {'descricao': 'Loja', 'id': '8', 'link': 'loja', 'qtde': '8'}, {'descricao': 'Lote / Terreno', 'id': '3', 'link': 'lote_terreno', 'qtde': '339'}, {'descricao': 'Negócio/ Empresa', 'id': '20', 'link': 'negocio_empresa', 'qtde': '1'}, {'descricao': 'Outro', 'id': '14', 'link': 'outro', 'qtde': '7'}, {'descricao': 'Ponto Comercial', 'id': '22', 'link': 'ponto_comercial', 'qtde': '6'}, {'descricao': 'Prédio', 'id': '16', 'link': 'predio', 'qtde': '2'}, {'descricao': 'Salão', 'id': '24', 'link': 'salao', 'qtde': '1'}, {'descricao': 'Sítio e Chácara', 'id': '5', 'link': 'sitio_chacara', 'qtde': '208'}, {'descricao': 'Sobrado', 'id': '10', 'link': 'sobrado', 'qtde': '362'}], 'link': 'venda', 'titulo': 'Comprar'}, {'itens': [{'descricao': 'Apartamento', 'id': '1', 'link': 'apartamento', 'qtde': '173'}, {'descricao': 'Área', 'id': '4', 'link': 'area', 'qtde': '4'}, {'descricao': 'Barracão / Galpão', 'id': '11', 'link': 'barracao_galpao', 'qtde': '53'}, {'descricao': 'Casa', 'id': '2', 'link': 'casa', 'qtde': '69'}, {'descricao': 'Conjunto Comercial', 'id': '9', 'link': 'conjunto_comercial', 'qtde': '39'}, {'descricao': 'Fazenda', 'id': '6', 'link': 'fazenda', 'qtde': '1'}, {'descricao': 'Kitinete', 'id': '12', 'link': 'kitinete', 'qtde': '4'}, {'descricao': 'Loja', 'id': '8', 'link': 'loja', 'qtde': '35'}, {'descricao': 'Lote / Terreno', 'id': '3', 'link': 'lote_terreno', 'qtde': '18'}, {'descricao': 'Negócio/ Empresa', 'id': '20', 'link': 'negocio_empresa', 'qtde': '1'}, {'descricao': 'Outro', 'id': '14', 'link': 'outro', 'qtde': '26'}, {'descricao': 'Ponto Comercial', 'id': '22', 'link': 'ponto_comercial', 'qtde': '6'}, {'descricao': 'Prédio', 'id': '16', 'link': 'predio', 'qtde': '6'}, {'descricao': 'Salão', 'id': '24', 'link': 'salao', 'qtde': '5'}, {'descricao': 'Sítio e Chácara', 'id': '5', 'link': 'sitio_chacara', 'qtde': '3'}, {'descricao': 'Sobrado', 'id': '10', 'link': 'sobrado', 'qtde': '26'}], 'link': 'locacao', 'titulo': 'Alugar'}, {'itens': [], 'link': 'locacao_dia', 'titulo': 'Alugar Dia'}]}}, 'principal': 1}
    args = {}
    args['teste'] = 1
    args['dias'] = 30
    imoveis = Imoveis(args,contato).itens['itens']
    return {'cidades':cidades, 'contato':contato, 'imoveis':imoveis, 'uteis':Uteis(args)}



def test_retorna_array_imovel_quando_campos_validos(inicia):
    corpo = Corpo_email(inicia['cidades'],inicia['contato'],inicia['imoveis'],inicia['uteis'])
    valor_campo = corpo._set_campos(inicia['imoveis']['itens'][0])
    assert valor_campo['classe'] == inicia['imoveis']['itens'][0]['tipo_negocio']

def test_retorna_zero_quando_set_tipo_negocio(inicia):
    corpo = Corpo_email(inicia['cidades'],inicia['contato'],inicia['imoveis'],inicia['uteis'])
    valor_campo = corpo._set_tipo_negocio_int()
    assert valor_campo == 0

def test_retorna_titulo_quando_html_corpo(inicia):
    corpo = Corpo_email(inicia['cidades'],inicia['contato'],inicia['imoveis'],inicia['uteis'])
    valor_campo = corpo._set_titulo_relacionado(inicia['imoveis']['itens'][0])
    imoveis = corpo._set_imoveis_corpo()
    c = corpo._set_html_corpo(imoveis)
    assert valor_campo in c

def test_deve_retornar_seis_imoveis_corpo_quando_carrega_corpo_html(inicia):
    corpo_email = Corpo_email(inicia['cidades'], inicia['contato'], inicia['imoveis'], inicia['uteis'])
    imoveis = corpo_email._set_imoveis_corpo()
    assert imoveis.count('<td>') == 6

def test_deve_retornar_array_images_quando_envia_imovel(inicia):
    corpo_email = Corpo_email(inicia['cidades'], inicia['contato'], inicia['imoveis'], inicia['uteis'])
    images = corpo_email._set_image(inicia['imoveis']['itens'][0])
    assert len(images)
