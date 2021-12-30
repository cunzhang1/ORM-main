# Software Architecture and Design Patterns -- Lab 3 starter code
# Copyright (C) 2021 Hui Lan

import model

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship, sessionmaker, clear_mappers

metadata = MetaData()

articles = Table(
    'articles',
    metadata,
    Column('article_id', Integer, primary_key=True, autoincrement=True),
    Column('text', String(10000)),
    Column('source', String(100)),
    Column('date', String(10)),
    Column('level', Integer, nullable=False),
    Column('question', String(1000)),
    )


users = Table(
    'users',
    metadata,
    Column('username', String(100), primary_key=True),
    Column('password', String(64)),
    Column('start_date', String(10), nullable=False),
    Column('expiry_date', String(10), nullable=False),
    )

newwords = Table(
    'newwords',
    metadata,
    Column('word_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(100), ForeignKey('users.username')),
    Column('word', String(20)),
    Column('date', String(10)),
    )

readings = Table(
    'readings',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(100), ForeignKey('users.username')),
    Column('article_id', Integer, ForeignKey('articles.article_id')),
    )


def start_mappers(): 
    metadata.create_all(create_engine('sqlite:///EnglishPalDatabase.db'))
    mapper(model.User, users)
    mapper(model.NewWord, newwords)
    mapper(model.Article, articles)
    mapper(model.Reading, readings)
