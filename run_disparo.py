
import sys

from app.argumentos import Argumentos
from app.disparos import Disparos

args = Argumentos().get()

# args['localhost'] = 1
args['teste'] = 1
args['dias'] = 60
args['qtde'] = 5

Disparos(args).set()