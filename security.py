from werkzeug.security import safe_str_cmp
from models.user import UserModel
import bcrypt


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
