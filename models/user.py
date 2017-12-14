from db import db
import bcrypt
import logging


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(25), unique=True)
    hashed_password = db.Column(db.String())
    role = db.Column(db.String(), default='ROLE_STANDARD_USER')

    def __init__(self, first_name, last_name, email, username, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password.encode('utf-8')
        self.hashed_password = bcrypt.hashpw(
            self.password, bcrypt.gensalt(10)).decode('utf-8')
        self.role = role

    def json_user(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'username': self.username,
            'role': self.role
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
