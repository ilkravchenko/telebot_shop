# Импортирую класс HandlerCommands обработка комманд
from handlers.handler_com import HandlerCommands
# Импортирую класс HandlerAllText обработка нажатия на кнопки и иные сообщения
from handlers.handler_all_text import HandlerAllText
# импортируем класс HandlerInlineQuery обработка нажатия на кнопки инлайн
from handlers.handler_inline_query import HandlerInlineQuery

class HandlerMain:
    """
    Клас компоновщик
    """
    def __init__(self, bot):
        # Получаю нашего бота
        self.bot = bot
        # Здесь будет инициализация обработчиков
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        # Здесь будет запуск обработчиков
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()