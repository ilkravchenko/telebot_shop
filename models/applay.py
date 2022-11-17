# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String

from data_base.dbcore import Base


class Applay(Base):
    """
    Класс для создания таблицы "Оформленных заказов"
    основан на декларативном стиле SQLAlchemy
    """
    #название таблицы
    __tablename__ = 'applay'
    # поля таблицы
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    phone = Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    def __str__(self):
        return f"Номер-{self.phone}, айди товара-{self.product_id}, количество-{self.quantity}"
