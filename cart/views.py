from flask import Blueprint
from flask import request
import logging
from app import db
from models import Cart, UserModel, CartItem, OrderItem, Orders, BookModel

cart_bp = Blueprint('cart_bp', __name__)
logging.basicConfig(filename="cart.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@cart_bp.route('/addcart', methods=['POST'])
def add_cart():
    try:
        data = request.get_json()
        book_list = data.get("list_of_books")
        cart = Cart.query.filter_by(user_id=data.get("user_id"), status=0).first()
        if cart:
            cart.total_quantity = cart.total_quantity + data.get('total_quantity')
            cart.total_price = cart.total_price + data.get('total_price')
            db.session.commit()
        else:
            cart = Cart(total_quantity=data.get("total_quantity"), total_price=data.get("total_price"),
                        user_id=data.get("user_id"), status=0)
            db.session.add(cart)
            db.session.commit()
        for book in book_list:
            cart_item = CartItem(cart_id=cart.cart_id, user_id=cart.user_id, book_id=book.get("book_id"),
                                 quantity=book.get("quantity"))
            db.session.add(cart_item)
            db.session.commit()
        return {"message": "Cart added successfully"}, 200
    except Exception as error:
        db.session.rollback()
        logger.exception(error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400


@cart_bp.route('/viewcart', methods=['POST'])
def get_cart():
    try:
        data = request.get_json()
        cart_items = db.session.query(CartItem, Cart, BookModel).filter(CartItem.cart_id == Cart.cart_id,
                                                                        CartItem.user_id == data.get("user_id"),
                                                                        Cart.status == 0,
                                                                        BookModel.id == CartItem.book_id).all()
        if cart_items:
            detail_of_Cart = {"Cart_id": cart_items[0].Cart.cart_id,
                              "total_quantity": cart_items[0].Cart.total_quantity,
                              "total_price": cart_items[0].Cart.total_price, "book_list": []}
            list_of_book = []
            for book in cart_items:
                book_dict = {"book_id": book.BookModel.id, "author": book.BookModel.author,
                             "price": book.BookModel.price, "quantity": book.CartItem.quantity}
                list_of_book.append(book_dict)
            detail_of_Cart.update({"book_list": list_of_book})
            return {"user_id": data.get("user_id"), "Cart Items": detail_of_Cart}
        return {"message": "User id not exist or may be inactive"}
    except Exception as error:
        logger.exception(error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400


@cart_bp.route('/addtoorder', methods=['POST'])
def add_cart_to_order():
    try:
        data = request.get_json()
        cart = db.session.query(CartItem, Cart).filter(CartItem.cart_id == Cart.cart_id,
                                                       CartItem.user_id == data.get("user_id"),
                                                       CartItem.cart_id == data.get("cart_id"), Cart.status == 0).all()
        if cart:
            order = Orders(total_price=cart[0].Cart.total_price, quantity=cart[0].Cart.total_quantity,
                           user_id=cart[0].Cart.user_id, status=cart[0].Cart.status)
            db.session.add(order)
            db.session.commit()

            for cart_item in cart:
                order_item = OrderItem(order_id=order.order_id, user_id=cart_item.CartItem.user_id,
                                       book_id=cart_item.CartItem.book_id, status=cart_item.Cart.status,
                                       quantity=cart_item.CartItem.quantity)
                db.session.add(order_item)
                db.session.commit()

            cart[0].Cart.status = 1
            db.session.commit()
            return {"message": "Cart Item Added to Order Successfully"}, 200
        return {"message": "Cart addition failed!! may be status is inactive or user_id or cart_id is Wrong!!!"}
    except Exception as error:
        logger.exception(error)

        return {"message": "Exception occurred", "error": str(error)}, 400
