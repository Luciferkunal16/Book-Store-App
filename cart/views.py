# from flask import Blueprint
# from flask import request
# from sqlalchemy.dialects.postgresql import psycopg2
# import logging
# from app import db
# from models import Cart, CartItem
#
# cart_bp = Blueprint('cart_bp', __name__)
# logging.basicConfig(filename="cart.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# @cart_bp.route('/addcart', methods=['POST'])
# def add_cart():
#     try:
#         data = request.get_json()
#         name = data.get("name")
#         cart = Cart(total_quantity=data.get("total_quantity"), total_price=data.get("total_price"),
#                     user_id=data.get("user_id"))
#         cart.status = 0
#         db.session.add(cart)
#         db.session.commit()
#         return {"message": "cart added"}
#     except (Exception, psycopg2.Error) as error:
#         logger.exception(error)
#         return {"message": "Data insertion Failed", "error": str(error)}, 400
