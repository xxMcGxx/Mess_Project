import socket
import sys
import argparse
import json
import logging
import logs.config_server_log
from errors import IncorrectDataRecivedError
from common.variables import *
from common.utils import *


#Инициализация логирования сервера.
server_logger = logging.getLogger('server')

# Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта, проверяет корректность, возвращает \
#                                                                                       словарь-ответ для клиента
def process_client_message(message):
    server_logger.debug(f'Разбор сообщения от клиента : {message}')
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
        server_logger.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. Допустимы адреса с 1024 до 65535.')
        exit(1)
    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port} , адрес с которого принимаются подключения: {listen_address}. Если адрес не указан, принимаются соединения с любых адресов.')
    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        server_logger.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = get_message(client)
            server_logger.debug(f'Получено сообщение {message_from_cient}')
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            server_logger.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            server_logger.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            server_logger.error(f'Не удалось декодировать Json строку, полученную от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            server_logger.error(f'От клиента {client_address} gриняты некорректные данные. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
