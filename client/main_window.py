from PyQt5.QtWidgets import QMainWindow, qApp
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys

sys.path.append('../')
from client.main_window_conv import Ui_MainClientWindow
from client.add_contact import AddContactDialog


# Класс основного окна
class ClientMainWindow(QMainWindow):
    def __init__(self, database , transport):
        super().__init__()
        self.database = database
        self.transport = transport

        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        # Кнопка "Выход"
        self.ui.menu_exit.triggered.connect(qApp.exit)

        # "добавить контакт"
        self.ui.btn_add_contact.clicked.connect(self.add_contact)
        self.ui.menu_add_contact.triggered.connect(self.add_contact)

        # Дополнительные требующиеся атрибуты
        self.contacts_model = None

        self.clients_list_update()

        self.show()

    # Функция обновляющяя контакт ликт
    def clients_list_update(self):
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    # Функция добавления контакта
    def add_contact(self):
        global select_dialog
        select_dialog = AddContactDialog()

        # Заполняем список возможных контактов разницей между всеми пользователями и
        def possible_contacts_update(window, base):
            # множества всех контактов и контактов клиента
            contacts_list = set(base.get_contacts())
            users_list = set(base.get_users())
            # составляем модель из разницы данных множеств
            possible_contacts_model = QStandardItemModel()
            for user in users_list - contacts_list:
                user = QStandardItem(user)
                user.setEditable(False)
                possible_contacts_model.appendRow(user)
            window.selector.setModel(possible_contacts_model)

        possible_contacts_update(select_dialog, self.database)

        # Обновлялка возможных контактов. Обновляет таблицу известных пользователей,
        # затем содержимое предполагаемых контактов
        def update_possible_contacts(self):
            try:
                users_list = user_list_request(sock, username)
            except ServerError:
                logger.error('Ошибка запроса списка известных пользователей.')
            else:
                database.add_users(users_list)

        select_dialog.show()
