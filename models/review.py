# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Float, ForeignKey
# импортирую модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# импортирую модель продуктов для связки моделей
from models.product import Products

from data_base.dbcore import Base


class Review(Base):
    """
    Класс для создания таблицы "Акции",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'reviews'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    review = Column(String)
    product_id = Column(Integer, ForeignKey('product.id'))

    # для каскадного удаления данных из таблицы
    products = relationship(
        Products,
        backref=backref('review',
                        uselist=True,
                        cascade='delete, all'))

    def __str__(self):
        return f"{self.review}"
