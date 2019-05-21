import sys
import json
import socket
import time
from common.variables import *
from common.utils import *


# Функция генерирует запрос о присутствии клиента
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def main():
    # Загружаем параметы коммандной строки
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    answer = get_message(transport)
    print(answer)


if __name__ == '__main__':
    main()
