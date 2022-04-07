import psycopg2
import psycopg2.extras
import logging
from flask import request
from flask import Blueprint

order_bp = Blueprint('order_bp', __name__)
connection = psycopg2.connect(user="postgres",
                              password="kunal123",
                              database="bookstore")
cursor = connection.cursor()

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
            add_to_order_command = "insert into orders (total_price,quantity,user_id,status) values ({},{},{}," \
                                   "{}) returning order_id".format(
                data.get("total_price"), total_quantity, data.get("user_id"), data.get("status"))
            cursor.execute(add_to_order_command)
            id_of_new_order = cursor.fetchone()[0]

            for book in book_list:
                add_to_order_item_command = "insert into order_item (order_id,user_id,book_id,status,quantity) values " \
                                            "({},{},{},{},{})".format(
                    id_of_new_order, data.get("user_id"), book.get("book_id"), data.get("status"), book.get("quantity"))
                cursor.execute(add_to_order_item_command)
            connection.commit()
            return {"message": "Data inserted Successfully"}, 200
        return {"message": "Data insertion Unsuccessfull because quantity of books  and total quantity not matching"}
    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        cursor.execute("ROLLBACK")
        connection.commit()
        print("Failed to insert record into mobile table", error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400


@order_bp.route("/getorder", methods=['POST'])
def get_order():
    try:
        data = request.get_json()
        get_order_command = "select order_item.book_id,books.price,books.author ,order_item.quantity from orders " \
                            "inner join order_item on orders.order_id=order_item.order_id  join books on " \
                            "order_item.book_id=books.id where orders.order_id={}".format(
            data.get("order_id"))
        cursor.execute(get_order_command)
        order_data = cursor.fetchall()
        if order_data:
            list_of_order = list()
            for line in order_data:
                list_of_order.append({"book_id": line[0], "price": line[1], "author": line[2],
                                      "quantity": line[3]})

            return {"order_id": data.get("order_id"), "order_list": list_of_order}
        return {"message": "Wrong order_id is given"}

    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        print(error)
        return {"message": "Fetching data Failed", "error": str(error)}, 400


@order_bp.route("/deleteorder", methods=['DELETE'])
def delete_order():
    try:
        data = request.get_json()
        order_id = data.get("order_id")
        delete_order_command = "DELETE FROM orders where order_id = {} returning order_id".format(order_id)
        cursor.execute(delete_order_command)
        deleted_item_id = cursor.fetchone()
        if deleted_item_id:
            connection.commit()
            return {"message": "Deletion Successfully done"}
        return {"message": "Order doesn't Exists!!! you entered wrong order_id"}

    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        print(error)
        return {"message": "Deletion Failed Exception occurred ", "error": str(error)}, 400


@order_bp.route("/getorderbyuid", methods=['POST'])
def get_order_by_user_id():
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = request.get_json()
        user_id = data.get("user_id")
        get_order_command = "select orders.order_id,orders.quantity as total_quantity,orders.total_price," \
                            "order_item.book_id,books.price,books.author ,order_item.quantity from orders inner join " \
                            "order_item on orders.order_id=order_item.order_id  join books on " \
                            "order_item.book_id=books.id where orders.user_id={}".format(
            user_id)
        cursor.execute(get_order_command)
        dict_of_data = cursor.fetchall()
        list_of_orders = list()
        temp = 0
        for line in dict_of_data:
            if temp != line["order_id"]:
                list_of_book = list()
                order = {"order_id": line["order_id"], "total quantity": line["total_quantity"],
                         "total_price": line["total_price"], "list_of_ordered_items": []}
                book = {"book_id": line["book_id"], "author": line["author"], "quantity": line["quantity"],
                        "price": line["price"]}
                list_of_book.append(book)
                order.update({"list_of_ordered_items": list_of_book})
                list_of_orders.append(order)
                temp = line["order_id"]
            else:
                book = {"book_id": line["book_id"], "author": line["author"], "quantity": line["quantity"],
                        "price": line["price"]}
                list_of_book.append(book)
        return {"user_id": user_id, "order_list": list_of_orders}
    except (Exception, psycopg2.Error) as error:
        logger.exception(error)
        print(error)
        return {"message": "Fetching data Failed", "error": str(error)}, 400
