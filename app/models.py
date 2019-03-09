from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    username = db.Column(db.String(30),index = True, unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True)
    DOB = db.Column(db.String(15))
    real_name = db.Column(db.String(20))
    user_profile = relationship("User_profile",uselist=False, back_populates="user")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class User_profile(db.model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_pic = db.Column(db.LargeBinary(length=2048))
    user_plan = db.Column(db.String(300))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="user_profile")

    def __repr__(self):
        return '<User %r>' % self.user
