# Software Architecture and Design Patterns -- Lab 3 starter code
# Copyright (C) 2021 Hui Lan

import pytest
import orm
import model

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers


@pytest.fixture
def engine():
    engine = create_engine('sqlite:///EnglishPalDatabase.db') # use your own path
    # engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3307/test?charset=utf8')     
    return engine


@pytest.fixture
def get_session(engine):
    orm.start_mappers()
    yield sessionmaker(bind=engine)
    clear_mappers()


@pytest.fixture
def prepare_data():
    engine = create_engine('sqlite:///EnglishPalDatabase.db')  
    orm.start_mappers()
    orm.metadata.drop_all(engine)
    orm.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    # add users
    session.add(model.User(username='mrlan', password='12345', start_date='2021-05-14'))
    session.add(model.User(username='lanhui', password='Hard2Guess!', start_date='2021-05-15'))
    session.add(model.User(username='hui', password='G00d@English:)', start_date='2021-05-30'))
    session.commit()

    # add words
    session.add(model.NewWord(username='lanhui', word='starbucks', date='2021-05-15'))
    session.add(model.NewWord(username='lanhui', word='luckin', date='2021-05-15'))
    session.add(model.NewWord(username='lanhui', word='secondcup', date='2021-05-15'))
    session.add(model.NewWord(username='mrlan',  word='costa', date='2021-05-15'))
    session.add(model.NewWord(username='mrlan',  word='timhortons', date='2021-05-15'))
    session.add(model.NewWord(username='hui',  word='frappuccino', date='2021-05-15'))
    session.commit()

    # add articles
    article = model.Article(article_id=1, text='THE ORIGIN OF SPECIES BY MEANS OF NATURAL SELECTION, OR THE PRESERVATION OF FAVOURED RACES IN THE STRUGGLE FOR LIFE', source='CHARLES DARWIN, M.A.', date='1859-01-01', level=5, question='Are humans descended from monkeys?')
    session.add(article)

    article = model.Article(article_id=2, text='THE ELEMENTS OF STYLE', source='WILLIAM STRUNK JR. & E.B. WHITE', date='1999-01-01', level=4, question='Who may benefit from this book?')
    session.add(article)

    session.commit()

    session.close()

    clear_mappers()