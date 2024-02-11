from .database import db
from flask_security import UserMixin



class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('UserRole', back_populates='role')

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    user = db.relationship('User', back_populates='roles')
    role = db.relationship('Role', back_populates='users')
  

class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_mail = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fs_uniquifier = db.Column(db.String(300), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)

    roles = db.relationship('UserRole', back_populates='user')

    # def __init__(self, u_mail, password, fs_uniquifier):
    #     self.u_mail = u_mail
    #     self.password = password
    #     self.fs_uniquifier = fs_uniquifier

class List(db.Model):
    __tablename__ = "list"
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(20))
    list_disc = db.Column(db.String(200))


class Book(db.Model):
    __tablename__ = "book"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String)
    book_author = db.Column(db.String)
    pages_in_book = db.Column(db.Integer)
    price = db.Column(db.Integer)

