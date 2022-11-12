# Импортирую класс родитель
from handlers.handler import Handler
# Импортирую сообщения пользователю
from settings.message import MESSAGES


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие текстовые
    сообщения от нажатия на инлайн кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_product(self, call, code, chat_id):
        """
        Обрабатывает входящие запросы на нажатия инлайн кнопок товара
        """
        # Создаю запись в БД по факту заказа
        self.BD._add_orders(1, code, chat_id)

        self.bot.answer_callback_query(
            call.id, MESSAGES['product_order'].format(
                self.BD.select_single_product_name(code),
                self.BD.select_single_product_title(code),
                self.BD.select_single_product_price(code)),
            show_alert=True)

    def handle(self):
        # Обработчик запросов от нажатия на кнопки товара
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit:
                code = int(code)

            self.pressed_btn_product(call, code, call.from_user.id)