import subprocess
import ipaddress
import re

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
        ping = subprocess.run(['ping' , str(dest) , '-n', '1'] , stdout=subprocess.PIPE)
        # Если 1, то доступен, если 0 то не доступен
        if reg.findall(ping.stdout.decode('cp866'))[0] == '1':
            print(f'Узел {dest} доступен')
        else:
            print(f'Узел {dest} недоступен')



if __name__ == '__main__':
    host_ping(['80.51.1.1' , 'localhost' , 'google.com' , '192.168.1.113'])

