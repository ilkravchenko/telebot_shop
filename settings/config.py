import os
# импортирую емодзи
from emoji import emojize

# TOKEN
TOKEN = '5692470746:AAG7EGor7oEU3o1CcFRT8Oy0o2l65makdpU'
# Название БД
NAME_DB = 'products.db'
# version
VERSION = '0.0.1'
# Author
AUTHOR = 'Illia Kravchenko'

# родительськая директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: Информация о магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'PHONES': emojize(':iphone: Телефоны', language='alias'),
    'COMPUTERS': emojize(':computer: Компьютеры', language='alias'),
    'TV': emojize(':tv: Телевизоры', language='alias'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ПОКУПКА'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽', language='alias'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼', language='alias'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'PHONES': 1,
    'COMPUTERS': 2,
    'TV': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}