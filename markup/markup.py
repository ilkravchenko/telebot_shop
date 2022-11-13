# Импортирую специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# Импортирую настройки и утилиты
from settings import config
# Импортирую класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """

    # Инициализация разметки
    def __init__(self):
        self.markup = None
        # Инициализирую менеджер для работы с БД
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0, user_id=None):
        """
        Создает и возвращает кнопку по входным параметрам
        """

        if name == "AMOUNT_ORDERS":
            config.KEYBOARD["AMOUNT_ORDERS"] = f"{step + 1} {'из'} {str(self.BD.count_rows_order(user_id))}"

        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = f"{quantity}"

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn("CHOOSE_GOODS")
        itm_btn_2 = self.set_btn("INFO")
        itm_btn_3 = self.set_btn("SETTINGS")
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню "О магазине"
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кнопок в меню "Настройки"
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # Расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    @staticmethod
    def remove_menu():
        """
        Функция удаляет данны кнопки и возвращает ее
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок в меню "Выбор товара"
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn("PHONES"))
        self.markup.add(self.set_btn("COMPUTERS"))
        self.markup.add(self.set_btn("TV"))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))

        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает  возвращает инлайн кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name), callback_data=(name.id))

    def set_select_category(self, category):
        """
        Создает разметку кнопок в выбраной категории
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # Загружаем в название инлайн кнопок данные
        # с БД в соответствии с категорией товара
        for itm in self.BD.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(itm))

        return self.markup

    def order_menu(self, step, quantity, user_id):
        """
        Создает разметку кнопок в заказе товара
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity, user_id)
        itm_btn_4 = self.set_btn('UP', step, quantity)
        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity, user_id)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLAY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)

        # Расположение кнопок
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup