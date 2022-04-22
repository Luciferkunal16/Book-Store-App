import logging
from io import StringIO

import pandas as pd
import io

from models import create_book, BookModel, db
from flask import request, Blueprint, jsonify
import csv

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
        if not book:
            return {"message": "Book Updation UnSuccessfull!!! No book found with the same name"}
        book.price = data.get("price")
        book.author = data.get("author")
        db.session.commit()
        return {"message": "Book Updated Successfully"}, 201
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
        if not book:
            return {"message": "Book Deletion Unsuccessfull!!! No book found with the same name"}
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book Deleted Successfully"}, 200
    except Exception as err:
        logger.exception(err)
        return {"message": "Book Deletion Unsuccessfull!!! Exception Occurred", "error": str(err)}, 400


@book_bp.route('/addbookcsv', methods=['POST'])
def add_book_by_csv():
    """
    for adding book to database
    through csv
    :return: status
    """

    try:
        with io.TextIOWrapper(request.files["file"], encoding="utf-8", newline='\n') as text_file:
            read = csv.reader(text_file)
            for row in read:
                if BookModel.query.filter_by(name=row[0]).first():
                    print(row[0])
                    logger.exception("Book already exist in database,Book name-{}".format(row[0]))
                else:
                    book = BookModel(name=row[0], author=row[1], price=row[2])
                    db.session.add(book)
                    db.session.commit()

            return {"message": "Book added successfully "}
    except Exception as e:
        return {"message": "Exception occurred", "error": str(e)}
