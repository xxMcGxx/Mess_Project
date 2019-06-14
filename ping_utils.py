import subprocess
import ipaddress
import re
import tabulate


# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
def host_ping(targets):
    # Регулярное выражение, для поиска количество возвращённых пакетов.
    reg = re.compile('получено = ([10])')
    for target in targets:
        try:
            # Если там IP адрес, то:
            dest = ipaddress.ip_address(target)
        except ValueError:
            # Раз не IP, считаем, что адрес хоста.
            dest = target
        ping = subprocess.run(['ping', str(dest), '-n', '1'], stdout=subprocess.PIPE)
        # Если 1, то доступен, если 0 то не доступен
        if reg.findall(ping.stdout.decode('cp866'))[0] == '1':
            print(f'Узел {dest} доступен')
        else:
            print(f'Узел {dest} недоступен')


# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.

# Функция автономная, хотя можно использовать для проверки по списку предыдущую функцию.
def host_range_ping(start, end):
    try:
        start_ip = ipaddress.ip_address(start)
        end_ip = ipaddress.ip_address(end)
    except ValueError:
        print('Аргументами функции должны быть IP адреса в текстовом формате')
        return
    # Регулярное выражение, для поиска количество возвращённых пакетов.
    reg = re.compile('получено = ([10])')
    while start_ip <= end_ip:
        ping = subprocess.run(['ping', str(start_ip), '-n', '1'], stdout=subprocess.PIPE)
        # Если 1, то доступен, если 0 то не доступен
        if reg.findall(ping.stdout.decode('cp866'))[0] == '1':
            print(f'Узел {start_ip} доступен')
        else:
            print(f'Узел {start_ip} недоступен')
        start_ip = start_ip + 1


# Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
# (использовать модуль tabulate). Таблица должна состоять из двух колонок

# Функция автономная, хотя можно использовать для проверки по списку предыдущую функцию.
def host_range_ping_tab(start, end):
    try:
        start_ip = ipaddress.ip_address(start)
        end_ip = ipaddress.ip_address(end)
    except ValueError:
        print('Аргументами функции должны быть IP адреса в текстовом формате')
        return
    # Регулярное выражение, для поиска количество возвращённых пакетов.
    reg = re.compile('получено = ([10])')
    rez = [('Узел' , 'Результат')]
    while start_ip <= end_ip:
        ping = subprocess.run(['ping', str(start_ip), '-n', '1'], stdout=subprocess.PIPE)
        # Если 1, то доступен, если 0 то не доступен
        if reg.findall(ping.stdout.decode('cp866'))[0] == '1':
            rez.append((start_ip , 'Доступен' ))
        else:
            rez.append((start_ip , 'Недоступен'))
        start_ip = start_ip + 1
    print(tabulate.tabulate(rez, headers='firstrow' , tablefmt='grid'))


if __name__ == '__main__':
    #host_ping(['80.51.1.1', 'localhost', 'google.com', '192.168.1.113'])
    #host_range_ping('8.8.8.5' , '8.8.8.10')
    host_range_ping_tab('8.8.8.5' , '8.8.8.10')
