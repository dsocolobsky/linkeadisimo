#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)