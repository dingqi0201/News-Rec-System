from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, func, BigInteger
from . import DBModel


class HOTNews(DBModel):
    __tablename__ = 'hot_news'
    news_id = Column(Integer, autoincrement=True, primary_key=True)
    news_words = Column(String(255), nullable=False)
    count = Column(Integer)
    month = Column(Integer)
    content = Column(String)


class HOMENews(DBModel):
    __tablename__ = 'home_news'
    news_id = Column(Integer, autoincrement=True, primary_key=True)
    news_words = Column(String(255), nullable=False)
    content = Column(String)


class TESTNews(DBModel):
    __tablename__ = 'test_news'
    user_id = Column(Integer)
    news_id = Column(Integer, autoincrement=True, primary_key=True)
    news_words = Column(String(255), nullable=False)
    month = Column(Integer)
    label = Column(Integer)
    content = Column(String)


class USERHistory(DBModel):
    __tablename__ = 'user_history'
    user_id = Column(Integer)
    news_id = Column(Integer, autoincrement=True, primary_key=True)
    news_words = Column(String(255), nullable=False)
    month = Column(Integer)
    content = Column(String)
