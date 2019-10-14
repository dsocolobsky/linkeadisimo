#!/usr/bin/env python3
from flask import Flask
from database import db

app = Flask(__name__)

@app.route('/')
def index():
    return 'linkeadisimo'

@app.route('/notfound')
def notfound():
    return 'page not found'

@app.teardown_appcontext
def shutdown(exception=None):
    db.remove()

if __name__ == '__main__':
    app.run()