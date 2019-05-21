import socket
import sys
from common.variables import *
from common.utils import *


# Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.

#Сначала обрабатываем порт:
try:
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        listen_port = DEFAULT_PORT
    if listen_port < 1024 or listen_port > 65535:
        raise ValueError
except IndexError:
    print('После параметра \'p\'- необходимо указать номер порта.')
    exit(1)
except ValueError:
    print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    exit(1)

# Затем загражем какой адрес слушать

try:
    if '-a' in sys.argv:
        listen_address = int(sys.argv[sys.argv.index('-a') + 1])
    else:
        listen_address = ''

except IndexError:
    print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    exit(1)


print(listen_port)
