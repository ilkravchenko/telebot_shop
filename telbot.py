# Импортирую функцию создания объекта бота
from telebot import TeleBot
# Импортирую основные настройки проекта
from settings import config
# Импортирую главный класс-обработчик бота
from handlers.handler_main import HandlerMain


class TelBot:
    """
    Основной класс телеграм бота(сервер), в основе которого
    используется библиотека pyTelegramBotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота
        """

        # Получаю токен
        self.token = config.TOKEN
        # Инициализирую бот на основе зарегистрированого токена
        self.bot = TeleBot(self.token)
        # Инициализирую обработчик событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        """
        Метод запускает основные события сервера
        """
        # Обработчик событий
        self.start()
        # Служит для запуска бота(работа в режиме нон-стоп)
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()