from models import UserModel, create_user,create_book,BookModel
from flask import jsonify, request
from app import app


@app.route('/register', methods=['POST'])
def register():
    """
    This function will take all require fields for user registration
    :return: Status of User Registration
    """

    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    if UserModel.query.filter_by(username=username).first():
        return jsonify({"message": "Username already Exists"})
    user = create_user(user_name=username, password=password, email=email)
    return jsonify({"message": "User Registration Successfull"})


@app.route("/login", methods=['POST'])
def login():
    """
    Function used for login the user into Book store
    :return: login Status
    """
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = UserModel.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "User Login Successful", "data": {"user_name": username}})
    else:
        return jsonify({"message": "Login Unsuccessfull !!! "})
