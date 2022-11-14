# Импортирую класс родитель
from handlers.handler import Handler

from settings.config import ADMIN
from settings.message import MESSAGES

class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /staet и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        Обрабатывает входящие /start команды
        """
        # self.BD._add_user(message.from_user.id ,message.from_user.first_name)
        if message.from_user.id == ADMIN:
            self.bot.send_message(message.chat.id,
                                  f"{message.from_user.first_name},"
                                  f"Добро пожаловать Админ!",
                                  reply_markup=self.keyboards.start_menu_admin())
        else:
            self.bot.send_message(message.chat.id,
                                  f"{message.from_user.first_name},"
                                  f"Здравствуйте! Добро пожаловать в наш магазин!",
                                  reply_markup=self.keyboards.start_menu())

    def pressed_btn_help(self, message):
        """
        Обрабатывает входящие /help команды
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.start_menu())

    def handle(self):
        # Обработчик(декоратор) сообщений
        # который обрабатывает входящие /start команды
        @self.bot.message_handler(commands=['start', 'help'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
            if message.text == '/help':
                self.pressed_btn_help(message)