from os import path
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base

from settings import config
from models.product import Products
from models.order import Order
from models.applay import Applay
from settings import utility

class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance

class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        """
        Возвращает все строки товаров из категории
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        return result

    def select_all_applay(self):
        """
        Возвращает все строки заказов
        """
        result = self._session.query(Applay).all()
        self.close()
        return result

    def select_all_products(self, products='all'):
        """
        Возвращает все строки товаров из категории
        """
        if products == 'all':
            result = self._session.query(Products).all()
        else:
            for i in products:
                result = []
                result.append(str(self._session.query(Products).filter_by(id=i).one()))
        self.close()
        return result

    # Добавление юзера в таблицу
    def _add_applay(self, user_id, phone, product_id, quantity):
        """
        Метод заполнения заказа на отправку
        """
        applay = Applay(user_id=user_id, phone=phone, product_id=product_id, quantity=quantity)
        self._session.add(applay)
        self._session.commit()
        self.close()


    # Работа с заказом
    def _add_orders(self, quantity, product_id, user_id,):
        """
        Метод заполнения заказа
        """
        # Получаю список всех product_id
        all_in_product = self.select_all_product_id(user_id)
        # Если есть даные в списке, обновляю таблицы заказа и продуктов
        if product_id in all_in_product:
            quantity_order = self.select_order_quantity(product_id, user_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # сли данных нет, создаю новый обьект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id = user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    def _add_product(self, name, title, price, quantity, category):
        """
        Метод добавления товара
        """
        try:
            product = Products(name=name, title=title, price=price,quantity=quantity,
                               is_active=1, category_id=category)

            self._session.add(product)
            self._session.commit()
            self.close()
        except:
            pass

    def change_product(self, product_id, name, title, price, quantity):
        """
        Метод изменения товара
        """
        try:
            self._session.query(Products).filter_by(id=product_id).update(
                {
                    Products.name: name,
                    Products.title: title,
                    Products.price: price,
                    Products.quantity: quantity
                })
            self._session.commit()
            self.close()
        except:
            pass

    def select_all_product_id(self, chat_id):
        """
        Возвращает все id товара в заказе
        """
        if chat_id != 'all':
            result = self._session.query(Order.product_id).filter_by(user_id=chat_id).all()
        else:
            result = self._session.query(Order.product_id).all()
        self.close()
        # конвертирую результат выборки
        return  utility._convert(result)

    def select_order_quantity(self, product_id, chat_id):
        """
        Вазвращает количество товара в заказе
        """
        result = self._session.query(Order.quantity).filter_by(user_id=chat_id).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указаной позиции заказа
        в соответствии с номером товара - product_id
        """
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - rownum
        Этот номер определфется при выборе товара в самом боте
        """
        result = self._session.query(Products.quantity).filter_by(
            id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, product_id, name, value):
        """
        Обновляет данные в таблице товара
        в соответствии с номером товара - product_id
        """
        result = self._session.query(Products).filter_by(
            id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        """
        Возвращает название товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """
        Возвращает производителя товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Возвращает цену товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def count_rows_order(self, chat_id):
        """
        Возвращает количество позиций в заказе
        """
        result = self._session.query(Order).filter_by(user_id=chat_id).count()
        self.close()
        return result

    def delete_order(self, product_id):
        """
        Удаляет данные указаной позиции в заказе
        """
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self, user_id):
        """
        Удаляет данные всего заказа в соответствии с user_id
        """
        all_in_order = self.select_all_order_id(user_id)
        result = []
        for itm in all_in_order:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self, user_id):
        """
        Собираю все id заказа
        """
        result = self._session.query(Order.id).filter_by(user_id=user_id).all()
        self.close()
        return utility._convert(result)

    def close(self):
        # Закрываем сессию
        self._session.close()
