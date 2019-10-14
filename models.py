#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<id={self.id}, title={self.title}, url={self.url}>'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __init__(self, title=None, url='/notfound'):
        self.title = title
        self.url = url

    def __repr__(self):
        return f'<id={self.id}, title={self.title}, url={self.url}>'

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(User(username="Flask", email="example@example.com", password="password"))
    db.session.add(Post(title="Test Post"))
    db.session.add(Post(title="Google", url="https://google.com"))
    db.session.commit()