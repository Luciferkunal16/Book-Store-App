import psycopg2
import psycopg2.extras
import logging
from flask import request
from flask import Blueprint

from app import db
from models import Orders, OrderItem

order_bp = Blueprint('order_bp', __name__)

logging.basicConfig(filename="order.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@order_bp.route('/addorder', methods=['POST'])
def add_order():
    try:
        data = request.get_json()
        total_quantity = data.get("quantity")
        book_list = data.get("book_list")
        if total_quantity == sum(book['quantity'] for book in book_list):
            order = Orders(total_price=data.get("total_price"), quantity=data.get("quantity"),
                           user_id=data.get("user_id"), status=data.get("status"))
            db.session.add(order)
            db.session.commit()
            for book in book_list:
                item = OrderItem(order_id=order.order_id, user_id=data.get("user_id"), book_id=book.get("book_id"),
                                 status=data.get("status"), quantity=book.get("quantity"))
                db.session.add(item)
                db.session.commit()
            return {"message": "Data inserted Successfully"}, 200
        return {"message": "Data insertion Unsuccessfull because quantity of books  and total quantity not matching"}
    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400


@order_bp.route("/getorder", methods=['POST'])
def get_order():
    try:
        data = request.get_json()
        order_list = OrderItem.query.filter_by(order_id=data.get("order_id")).all()

        list_of_order = list()
        if order_list:
            for book in order_list:
                list_of_order.append({"book_id": book.book_id, "price": book.book.price, "author": book.book.author,
                                      "quantity": book.quantity})

            return {"order_id": data.get("order_id"), "order_list": list_of_order}
        return {"message": "Wrong order_id is given"}
    except Exception as error:
        logger.exception(error)
        return {"message": "Fetching data Failed", "error": str(error)}, 400


@order_bp.route("/deleteorder", methods=['DELETE'])
def delete_order():
    try:
        data = request.get_json()
        order_id = data.get("order_id")
        order = Orders.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Deletion Successfully done"}
        return {"message": "Order doesn't Exists!!! you entered wrong order_id"}

    except Exception as error:
        logger.exception(error)
        return {"message": "Deletion Failed Exception occurred ", "error": str(error)}, 400


@order_bp.route("/getorderbyuid", methods=['POST'])
def get_order_by_user_id():
    try:
        data = request.get_json()
        order_list = OrderItem.query.filter_by(user_id=data.get("user_id"))
        temp = 0
        list_of_orders = list()
        for order in order_list:
            if temp != order.order_id:
                list_of_book = list()
                order_dict = {"order_id": order.order_id, "total quantity": order.orders.quantity,
                              "total_price": order.orders.total_price,
                              "list_of_ordered_items": []}
                books = {"book_id": order.book.id, "author": order.book.author, "quantity": order.quantity,
                         "price": order.book.price}
                list_of_book.append(books)
                order_dict.update({"list_of_ordered_items": list_of_book})
                list_of_orders.append(order_dict)
                temp = order.order_id
            else:
                books = {"book_id": order.book.id, "author": order.book.author, "quantity": order.quantity,
                         "price": order.book.price}
                list_of_book.append(books)
        return {"user_id": 1, "Order_list": list_of_orders}
    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        return {"message": "Fetching data Failed", "error": str(error)}, 400
