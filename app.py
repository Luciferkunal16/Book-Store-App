from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(example_blueprint)

app.config.from_object("settings")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kunal123@localhost/bookstore'
db = SQLAlchemy(app)


if __name__ == '__main__':
    from user.views import *
    from book.views import *
    app.run(debug=True)
