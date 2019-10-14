#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app

from models import User, Post

@app.route('/')
def index():
    lp = Post.query.all()
    return render_template('index.html', posts=lp)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    valid_login = do_login(request.form['user'], request.form['password'])
    if valid_login:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('notfound'))

@app.route('/notfound')
def notfound():
    return 'page not found'

def do_login(user, password):
    queried = None
    if '@' in user:
        queried = User.query.filter_by(email=user).first()
    else:
        queried = User.query.filter_by(username=user).first()
    
    return (queried is not None) and queried.password == password


if __name__ == '__main__':
    app.run()
