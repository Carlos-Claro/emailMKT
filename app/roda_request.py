from app.request import Request
from app.uteis import Uteis

uteis = Uteis(['localhost'])
uteis.set_keys()

request = Request(uteis)
data = {'filtro': {}}
data['filtro']['limit'] = 5
data['filtro']['dias'] = 60
data['url_tipo'] = 'contatos'
data['tipo'] = 'get'
request = request.request(data)
print(request)

