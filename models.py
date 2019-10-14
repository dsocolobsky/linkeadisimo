#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String)

    def __init__(self, title=None, url='/notfound'):
        self.title = title
        self.url = url

    def __repr__(self):
        return f'<id={self.id}, title={self.title}, url={self.url}>'

