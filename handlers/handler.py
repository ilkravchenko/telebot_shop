# Импортирую библиотеку abc для реализации абстракных классов
import abc
# Импортирую разметку клавиатуры и клавиш
from markup.markup import Keyboards
# Импортирую класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        # Получаю объект бота
        self.bot = bot
        # Инициализирю разметку кнопок
        self.keyboards = Keyboards()
        # Инициализирую менеджер для работы с БД
        self.BD = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
