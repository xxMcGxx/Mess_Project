import sys
sys.path.append('../')
from server import process_client_message
from common.variables import *
import unittest


# в сервере только 1 функция для тестирования
class TestServer(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}
    # ошибка если нет действия
    def test_no_action(self):
        self.assertEqual(process_client_message({TIME : '1.1' , USER : {ACCOUNT_NAME : 'Guest'}}), self.err_dict)
    # Ошибка если неизвестное действие
    def test_wrong_action(self):
        self.assertEqual(process_client_message({ACTION : 'Wrong' , TIME : '1.1' , USER : {ACCOUNT_NAME : 'Guest'}}), self.err_dict)
    # Ошибка, если  запрос не содержит штампа времени
    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION : PRESENCE , USER : {ACCOUNT_NAME : 'Guest'}}), self.err_dict)
    # Ошибка - нет пользователя
    def test_no_user(self):
        self.assertEqual(process_client_message({ACTION : PRESENCE ,TIME : '1.1' }), self.err_dict)
    # Ошибка - не Guest
    def test_unknown_user(self):
        self.assertEqual( process_client_message( {ACTION : PRESENCE , TIME : 1.1 , USER : {ACCOUNT_NAME : 'Guest1'}}) , self.err_dict)
    #  корректный запрос
    def test_ok_check(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

if __name__ == '__main__':
    unittest.main()


