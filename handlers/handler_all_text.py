# Импортирую ответ пользователю
from settings.message import MESSAGES
from settings import config
from settings import utility
# Импортирую класс родитель
from handlers.handler import Handler

class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # Шаг в заказе
        self.step = 0

    def pressed_btn_up(self,message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку up
        """
        # Получаю список всех товаров в заказе
        count = self.BD.select_all_product_id(message.from_user.id)
        # Получаю количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step], message.from_user.id)
        # Получаю количество конкретной позиции в продуков
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        # Если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # Вношу изменения в БД ордерc
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            #  Вношу изменения в БД продуктов
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        # Отправляю ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку down
        """
        # Получаю список всех товаров в заказе
        count = self.BD.select_all_product_id(message.from_user.id)
        # Получаю количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step], message.from_user.id)
        # Получаю количество конкретной позиции в продуков
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        # Если товар есть
        if quantity_product > 0:
            quantity_order -= 1
            quantity_product += 1
            # Вношу изменения в БД ордерc
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            #  Вношу изменения в БД продуктов
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        # Отправляю ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)


    def pressed_btn_x(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Удалить товар из заказа"
        """
        # Получает список всех товаров в заказе
        count = self.BD.select_all_product_id(message.from_user.id)
        # Если список не пуст
        if count.__len__() > 0:
            # Получаю количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step], message.from_user.id)
            # Получаю колтчество товара в конкретной аозиции заказа для возврата в продукт
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            # Вношу изменения в БД заказа
            self.BD.delete_order(count[self.step])
            # Вношу изменения в БД товара
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            # Уменьшаю шаг
            self.step -= 1

        count = self.BD.select_all_product_id(message.from_user.id)
        # Если список не пуст
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step], message.from_user.id)
            # Отправляет пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # Если товара нету в заказе
            self.bot.send_message(message.chat.id, MESSAGES["no_orders"],
                                  parse_mode="HTML",
                                  reply_markup=self.keyboards.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Предыдущий товар"
        """
        # Уменьшаю шаг пока шаг не будет равен "0"
        if self.step > 0:
            self.step -= 1
        # Получаю список всех товаров в заказе
        count = self.BD.select_all_product_id(message.from_user.id)
        quantity = self.BD.select_order_quantity(count[self.step], message.from_user.id)

        # Отправляю ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Следующий товар"
        """
        # Увеличиваю шаг пока шаг не будет равен количеству строк полей заказа с расчетом цены начиная с "0"
        if self.step < self.BD.count_rows_order(message.from_user.id)-1:
            self.step += 1
        # Получаю список всех товаров
        count = self.BD.select_all_product_id(message.from_user.id)
        # Получаю количество конкретного товара
        quantity = self.BD.select_order_quantity(count[self.step], message.from_user.id)

        # Ответ пользователю
        self.send_message_order(count[self.step],quantity, message)

    def pressed_btn_applay(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Оформить заказ"
        """
        # Отправляет ответ пользователю
        self.bot.send_message(message.chat.id,
                              MESSAGES['applay'].format(
                              utility.get_total_coast(self.BD, message.from_user.id),
                              utility.get_total_quantity(self.BD, message.from_user.id)),
                              parse_mode='HTML',
                              reply_markup=self.keyboards.category_menu())
        # Удаляю данные с таблицы заказа
        self.BD.delete_all_order(message.from_user.id)

    def pressed_btn_category(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Выбрать товар"
        """
        self.bot.send_message(message.chat.id, "Каталог товаров",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, "Выберите категорию",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_admin(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Меню Админа"
        """
        self.bot.send_message(message.chat.id, "Меню Админа",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id, "Выберите категорию",
                              reply_markup=self.keyboards.admin_menu())

    def pressed_btn_info(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "О магазине"
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Настройки"
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_admin_settings(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Настройки" в меню для админа
        """
        self.bot.send_message(message.chat.id, MESSAGES['admin_settings'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.admin_settings_menu())

    def pressed_btn_back(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Назад"
        """
        if message.from_user.id == config.ADMIN:
            self.bot.send_message(message.chat.id, "Вы вернулись назад",
                                  reply_markup=self.keyboards.start_menu_admin())
        else:
            self.bot.send_message(message.chat.id, "Вы вернулись назад",
                                  reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопки в каталоге товаров
        """
        self.bot.send_message(message.chat.id, "Категория " + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Заказ"
        """
        # Обнуляем данные шага
        self.step = 0
        # Получаем список всех товаров в заказе
        count = self.BD.select_all_product_id(message.from_user.id)
        # Получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step], message.from_user.id)

        # Отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step+1), parse_mode='HTML')
        self.bot.send_message(message.chat.id, MESSAGES['order'].format(
            self.BD.select_single_product_name(product_id),
            self.BD.select_single_product_title(product_id),
            self.BD.select_single_product_price(product_id),
            self.BD.select_order_quantity(product_id, message.from_user.id)),
                              parse_mode="HTML",
                              reply_markup=self.keyboards.order_menu(
                                  self.step, quantity, message.from_user.id))

    def pressed_btn_add_product(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Добавить товар"
        """
        self.bot.send_message(message.chat.id, "Введите сю информацию ниже через запятую!!!!!")
        self.bot.send_message(message.chat.id, "Какой категории товар желаете добавить?\n"
                                                              "1 - Телефоны\n"
                                                              "2 - Компьютеры\n"
                                                              "3 - Телевизоры\n"
                                               "для этого пункта введите только цыфру!!!!!")
        category = message.text
        self.bot.send_message(message.chat.id, "Введите название товара.")
        self.bot.send_message(message.chat.id, "Введите производителя товара.")
        self.bot.send_message(message.chat.id, "Введите цену товара.")
        self.bot.send_message(message.chat.id, "Введите количество товара.")
        self.bot.send_message(message.chat.id, "Вношу товар в базу данные, подождите сообщение об успешной операции")

        data_from_tg = message.text.split(",")
        category = data_from_tg[0]
        name = data_from_tg[1]
        title = data_from_tg[2]
        price = data_from_tg[3]
        quantity = data_from_tg[4]

        self.BD._add_product(name, title, price, quantity, category)


    def handle(self):
        """
        Обработчик(декоратор) сообщений,
        который обрабатывает входящие текстовые сообщения от нажатия кнопок
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            #*************** меню **************#

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            elif message.text == config.KEYBOARD['ADMIN_MENU']:
                self.pressed_btn_admin(message)

            elif message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            elif message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            elif message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            elif message.text == config.KEYBOARD["ORDER"]:
                # Если есть заказ
                if self.BD.count_rows_order(message.from_user.id) > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(
                        message.chat.id, MESSAGES['no_orders'],
                        parse_mode="HTML",
                        reply_markup=self.keyboards.category_menu())

            #*********** меню для Админа **************#

            elif message.text == config.KEYBOARD['ADD_PRODUCT']:
                self.pressed_btn_add_product(message)

            #elif message.text == config.KEYBOARD[CHANGE_PRODUCT]:
            #    self.pressed_btn_back(message)

            #*********** меню категирии товаров (Телефоны, компьютеры, телевизоры)***********#

            elif message.text == config.KEYBOARD["PHONES"]:
                self.pressed_btn_product(message, 'PHONES')

            elif message.text == config.KEYBOARD['COMPUTERS']:
                self.pressed_btn_product(message, 'COMPUTERS')

            elif message.text == config.KEYBOARD['TV']:
                self.pressed_btn_product(message, 'TV')

            #*********** меню закза *************#

            elif message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            elif message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            elif message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            elif message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            elif message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            elif message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_applay(message)
            else:
                self.bot.send_message(message.chat.id, message.text)