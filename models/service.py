# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, String, Float, ForeignKey
# импортирую модуль для связки таблиц
from sqlalchemy import relationship, backref
# импортирую модель продуктов для связки моделей
from models.product import Products

from data_base.dbcore import Base


class Service(Base):
    """
    Класс для создания таблицы "Услуги",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'services'

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    specification = Column(String)
    service_price = Column(Float)
    product_id = Column(Integer, ForeignKey('product.id'))

    # для каскадного удаления данных из таблицы
    products = relationship(
        Products,
        backref=backref('services',
                        uselist=True,
                        cascade='Delete, all'))

    def __str__(self):
        return f"{self.name} {self.service_price}\n{self.specification}"
