# компоненты из библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Boolean

from data_base.dbcore import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товара",
    основан на декаративном стиле SQLAlchemy
    """

    # название таблицы
    __tablename__ = 'category'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        """
        Метод возвращает строковое представление объектов класса
        """
        return self.name