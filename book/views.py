import logging
from models import create_book, BookModel, db
from flask import request, Blueprint


book_bp = Blueprint('book_bp', __name__)

logging.basicConfig(filename="book.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@book_bp.route('/addbook', methods=['POST'])
def add_book():
    """
    For adding book to database
    :return:add book status
    """
    try:
        data = request.get_json()
        name = data.get('name')
        author = data.get('author')
        price = data.get('price')
        if BookModel.query.filter_by(name=name).first():
            return {"message": "Book already Exists"}

        book = create_book(name, price, author)
        return {"message": "Book Added Successfully", "data": book.get_json()}, 201
    except Exception as err:
        logger.exception(err)
        return {"message": "Book Addition unsuccessfull", "error": str(err)}, 400


@book_bp.route("/getbook", methods=['GET'])
def get_book():
    """
    For getting list of all books
    :return:
    """
    try:
        books = BookModel.query.all()
        return {'Books': list(x.get_json() for x in books)}, 200
    except Exception as err:
        logger.exception(err)
        return {"message": "Exception occurred", "error": str(err)}, 400


@book_bp.route("/updatebook", methods=['PUT'])
def update_book():
    """
    For Updating the existing book inside the database
    :return: updated book
    """
    try:
        data = request.get_json()
        name = data.get('name')
        book = BookModel.query.filter_by(name=name).first()
        if book:
            book.price = data.get("price")
            book.author = data.get("author")
            db.session.commit()
            return {"message": "Book Updated Successfully"}, 201
        return {"message": "Book Updation UnSuccessfull!!! No book found with the same name"}
    except Exception as err:
        logger.exception(err)
        return {"message": "Book Updation UnSuccessfull!!! Exception Occurred", "error": str(err)}, 400


@book_bp.route("/deletebook", methods=['DELETE'])
def book_delete():
    """
    For deleting the book from Database
    :return: delete status
    """
    try:

        data = request.get_json()
        book = BookModel.query.filter_by(name=data.get('name')).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book Deleted Successfully"}, 200
        return {"message": "Book Deletion Unsuccessfull!!! No book found with the same name"}
    except Exception as err:
        logger.exception(err)
        return {"message": "Book Deletion Unsuccessfull!!! Exception Occurred", "error": str(err)}, 400


@book_bp.route('/addbookcsv', methods=['POST'])
def add_book_by_csv():
    """
    for adding book to database
    throuugh csv
    :return: status
    """

    try:
        data = request.get_json()
        if BookModel.query.filter_by(name=data.get("title")).first():
            return {"message": "Book already Exists"}
        book = BookModel(name=data.get("title"), price=int(data.get("price")), author=data.get("author"))
        db.session.add(book)
        db.session.commit()

        return {"message": "Book added successfully "}
    except Exception as e:
        return {"message": "Exception occurred", "error": str(e)}
