import datetime
import sys
import time

from app.argumentos import Argumentos
from app.disparos import Disparos
from app.logs import Logs

args = Argumentos().get()

# args['localhost'] = 1
args['teste'] = 1
args['dias'] = 60
args['qtde'] = 2
inicio = time.time()
qtde = 0
Disparos(args).set()
# while Disparos(args).set():
qtde += 1
fim = time.time()
tempo = fim - inicio
data = {
    'formato': 'geral',
    'arquivo': 'log',
    'data':{
        'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'message': f'Qtde de loops = {qtde} tempo {tempo}'
    }
}
Logs(data)
print(f'Qtde de loops = {qtde} tempo {tempo}')