from app import db
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import relationship


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(20))
    email = db.Column(db.String(30))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"{self.username}:{self.password}:{self.email}"


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))

    def __init__(self, name, price, author):
        self.name = name
        self.price = price
        self.author = author

    def get_json(self):
        return {"name": self.name, "price": self.price, "author": self.author}

def create_user(user_name, password, email):
    user = UserModel(user_name, password, email)
    db.session.add(user)
    db.session.commit()

    return user


def create_book(name, price, author):
    book = BookModel(name, price, author)
    db.session.add(book)
    db.session.commit()
    return book


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(Integer, primary_key=True)
    total_price = db.Column(Integer)
    quantity = db.Column(Integer)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    status = db.Column(Integer)

    user = relationship("UserModel")


class OrderItem(db.Model):
    __table__name = 'order_item'
    order_item_id = db.Column(Integer, primary_key=True)
    order_id = db.Column(Integer, ForeignKey('orders.order_id'))
    user_id = db.Column(Integer, ForeignKey('users.id'))
    book_id = db.Column(Integer, ForeignKey('books.id'))
    status = db.Column(Integer)
    quantity = db.Column(Integer)
    book = relationship("BookModel")
    orders = relationship("Orders")
