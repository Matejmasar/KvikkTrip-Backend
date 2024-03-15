from database import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
"""Implements the Users table """

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))

    @property
    def id(self):
        return self.id_user
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def create_user(cls, name, email, username, password):
        user = cls(name=name, email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def update_user(cls, user_id, new_name, new_email):
        user = cls.query.get(user_id)
        if not user:
            return None  # user not found

        if new_name is not None:
            user.name = new_name
        if new_email is not None:
            user.email = new_email
        db.session.commit()
        return user

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        if not user:
            return False  # User not found

        db.session.delete(user)
        db.session.commit()
        return True
    
    @classmethod
    def serialize(self):
       {
            'id': self.id_user,
            'username': self.name,
            'email': self.email
       }