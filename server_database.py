from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from common.variables import *
import datetime


# Класс - серверная база данных:
class ServerStorage:
    # Класс - отображение таблицы всех пользователей
    class AllUsers:
        def __init__(self, username):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.id = None

    # Класс - отображение таблицы активных пользователей:
    class ActiveUsers:
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    # Класс - отображение таблицы истории входов
    class LoginHistory:
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    def __init__(self):
        # Создаём движок базы данных
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу пользователей
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime)
                            )

        # Создаём таблицу активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        # Создаём таблицу истории входов
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    # Функция выполняющяяся при входе пользователя, записывает в базу факт входа
    def user_login(self, username, ip_address, port):
        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        rez = self.session.query(self.AllUsers).filter_by(name=username)

        # Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
        # Если нету, то создаздаём нового пользователя
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            # Комит здесь нужен, чтобы присвоился ID
            self.session.commit()

        # Теперь можно создать запись в таблицу активных пользователей о факте входа.
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        # и сохранить в историю входов
        history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        # Сохрраняем изменения
        self.session.commit()

    # Функция фиксирующая отключение пользователя
    def user_logout(self, username):
        # Запрашиваем пользователя, что покидает нас
        user = self.session.query(self.AllUsers).filter_by(name=username).first()

        # Удаляем его из таблицы активных пользователей.
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        # Применяем изменения
        self.session.commit()

    # Функция возвращает список известных пользователей со временем последнего входа.
    def users_list(self):
        # Запрос строк таблицы пользователей.
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
            )
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем кортежи имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращающаяя историю входов по пользователю или всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.name == username)
        # Возвращаем список кортежей
        return query.all()


# Отладка
if __name__ == '__main__':
    test_db = ServerStorage()
    # test_db.user_login('1111', '192.168.1.113', 8080)
    # test_db.user_login('McG2', '192.168.1.113', 8081)
    print(test_db.users_list())
    # print(test_db.active_users_list())
    # test_db.user_logout('McG')
    # print(test_db.login_history('re'))
