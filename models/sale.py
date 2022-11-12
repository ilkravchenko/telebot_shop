# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Float, ForeignKey
# импортирую модуль для связки таблиц
from sqlalchemy.orm import relationship, backref
# импортирую модель продуктов для связки моделей
from models.product import Products

from data_base.dbcore import Base


class Sale(Base):
    """
    Класс для создания таблицы "Акции",
    основан на декларативном стиле SQLAlchemy
    """
    #название таблицы
    __tablename__ = 'sales'

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    sale_price = Column(Float)
    product_id = Column(Integer, ForeignKey('product.id'))

    # для каскадного удаления данных из таблицы
    products = relationship(
        Products,
        backref=backref('sales',
                        uselist=True,
                        cascade='delete, all'))

    def __str__(self):
        return f"{self.name} {self.title} {self.sale_price}"