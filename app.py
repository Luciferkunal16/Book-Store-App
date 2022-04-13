from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kunal123@localhost/bookstore'
db = SQLAlchemy(app)


def register_blueprint():
    app.register_blueprint(user_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)

if __name__ == '__main__':
    from book.views import *
    from user.views import *
    from order.views import *
    from cart.views import *

    register_blueprint()
    app.run(debug=True)
