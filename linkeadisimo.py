#!/usr/bin/env python3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app

from models import User, Post

@app.route('/')
def index():
    lp = Post.query.all()
    return render_template('index.html', posts=lp)

@app.route('/notfound')
def notfound():
    return 'page not found'

if __name__ == '__main__':
    app.run()
