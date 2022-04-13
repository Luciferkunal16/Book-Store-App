from flask import Blueprint
from flask import request
import logging
from app import db
from models import Cart, UserModel, CartItem

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
        list_of_books = data.get("list_of_books")
        cart = Cart.query.filter_by(user_id=data.get("user_id"), status=0).first()
        if cart:
            cart.total_quantity = cart.total_quantity + data.get('total_quantity')
            cart.total_price = cart.total_price + data.get('total_price')
            db.session.commit()

            for book in list_of_books:
                cart_item = CartItem(cart_id=cart.cart_id, user_id=cart.user_id, book_id=book.get("book_id"))
                db.session.add(cart_item)
                db.session.commit()
            return {"message": "cart is updated"}
        cart = Cart(total_quantity=data.get("total_quantity"), total_price=data.get("total_price"),
                    user_id=data.get("user_id"), status=0)
        db.session.add(cart)
        db.session.commit()
        for book in list_of_books:
            cart_item = CartItem(cart_id=cart.cart_id, user_id=cart.user_id, book_id=book.get("book_id"))
            db.session.add(cart_item)
            db.session.commit()
        return {"message": "new cart added"}
    except Exception as error:
        logger.exception(error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400


@cart_bp.route('/viewcart', methods=['POST'])
def get_cart():
    try:
        data = request.get_json()
        cart_items = CartItem.query.filter_by(cart_id=data.get("cart_id")).all()
        items = [{"name": cart_items[0].user.username, "total_quantity": cart_items[0].cart.total_quantity,
                  "total_price": cart_items[0].cart.total_price}]

        return {"user_id": cart_items[0].user_id, "cart_items": items}
    except Exception as error:
        logger.exception(error)
        return {"message": "Data insertion Failed", "error": str(error)}, 400
