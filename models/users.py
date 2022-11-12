# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String

from data_base.dbcore import Base


class Users(Base):
    """
    Класс для создания таблицы "Юзеров"
    основан на декларативном стиле SQLAlchemy
    """
    #название таблицы
    __tablename__ = 'users'
    # поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String)
