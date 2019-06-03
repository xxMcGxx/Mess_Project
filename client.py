import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log
from common.variables import *
from common.utils import *
from errors import IncorrectDataRecivedError, ReqFieldMissingError , ServerError
from decos import log

# Инициализация клиентского логера
logger = logging.getLogger('client')


# Функция запрашивает текст сообщения и возвращает его. Так же завершает работу при вводе подобной комманды
def create_message():
    pass




# Функция генерирует запрос о присутствии клиента
@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# Функция разбирает ответ сервера
@log
def process_ans(message):
    logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


# Создаём парсер аргументов коммандной строки и читаем параметры, возвращаем 3 параметра
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        logger.critical(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
        exit(1)

    return server_address, server_port, client_mode


def main():
    # Загружаем параметы коммандной строки
    server_address, server_port, client_mode = arg_parser()

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, режим работы: {client_mode}')

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(answer)
    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг запрос на подключение.')
    else:
        # Если соединение с сервером установлено корректно, начинаем обмен с ним, согласно требуемому режиму.
        print('Ok') # Todo


if __name__ == '__main__':
    main()
