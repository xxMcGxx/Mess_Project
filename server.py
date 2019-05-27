import socket
import sys
import argparse
import json
from errors import IncorrectDataRecivedError
from common.variables import *
from common.utils import *


# Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта, проверяет корректность, возвращает \
#                                                                                       словарь-ответ для клиента
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and \
            message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    else:
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


# Парсер аргументов коммандной строки.
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        print('Необходимо указать порт в диапазоне от 1024 до 65535.')
        exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            send_message(client, response)
            client.close()
        except json.JSONDecodeError:
            print('Не удалось декодировать Json строку.')
            client.close()
        except IncorrectDataRecivedError:
            print('Приняты некорректные данные.')
            client.close()


if __name__ == '__main__':
    main()
