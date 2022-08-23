import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    def __str__(self):
        return f'Publisher: {self.id}, {self.name}'

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")
    stock = relationship(Stock, backref="book")

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80))
    stock = relationship(Stock, backref="shop")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Таблицы базы созадны.')

def load_tables(file_name, session):
    with open(file_name, "r") as f:
        data = json.load(f)
        for i in data:
            if i['model'] == 'publisher':
                pub = Publisher(id=i['pk'], name=i['fields']['name'])
                session.add(pub)
            elif i['model'] == 'book':
                book = Book(id=i['pk'], title=i['fields']['title'], id_publisher=i['fields']['id_publisher'])
                session.add(book)
            elif i['model'] == 'shop':
                shop = Shop(id=i['pk'], name=i['fields']['name'])
                session.add(shop)
            elif i['model'] == 'stock':
                stock = Stock(id=i['pk'], id_shop=i['fields']['id_shop'], id_book=i['fields']['id_book'],
                              count=i['fields']['count'])
                session.add(stock)
            elif i['model'] == 'sale':
                sale = Sale(id=i['pk'], price=i['fields']['price'], date_sale=i['fields']['date_sale'],
                            count=i['fields']['count'], id_stock=i['fields']['id_stock'])
                session.add(sale)
    session.commit()
    print('Данные загружены')
