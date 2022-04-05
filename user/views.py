import logging
from models import UserModel, create_user
from flask import request
from utils import EmailService
from flask import Blueprint

user_bp = Blueprint('user_bp', __name__)

logging.basicConfig(filename="user.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@user_bp.route('/register', methods=['POST'])
def register():
    """
    This function will take all require fields for user registration
    :return: Status of User Registration
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if UserModel.query.filter_by(username=username).first():
            return {"message": "Username already Exists"}, 200
        create_user(user_name=username, password=password, email=email)
        EmailService.send_otp(email)
        return {"message": "User Registration Successfull"}, 200
    except Exception as err:
        logger.error(err)
        return {"mesage": "Registration Unscuccessfull!!! Exception Occured", "error": err}, 400


@user_bp.route("/login", methods=['POST'])
def login():
    """
    Function used for login the user into Book store
    :return: login Status
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = UserModel.query.filter_by(username=username, password=password).first()
        if not user:
            return {"message": "Login Unsuccessfull !!! "}, 200
        return {"message": "User Login Successful", "data": {"user_name": username}}, 200


    except Exception as err:
        logger.exception(err)
        return {"message": "Login Unsuccessfull!!! Exception Occurred ", "error": err}, 400
