**Lab 3**: The ORM Magic and The Service Layer
=================================================

**小组成员**

201932110118韩舒扬

201932110124李梁伟

201932110122黄士极

201932110121黄君杰


orm.py
=================================================
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


model.py
=================================================
# Software Architecture and Design Patterns -- Lab 3 starter code
# Copyright (C) 2021 Hui Lan

from dataclasses import dataclass


@dataclass
class Article:
    article_id:int
    text:str
    source:str
    date:str
    level:int
    question:str

class Reading:
    def __init__(self, username, article_id):
        self.username = username
        self.article_id = article_id

class NewWord:
    def __init__(self, username, word='', date='yyyy-mm-dd'):
        self.username = username
        self.word = word
        self.date = date


class User:
    def __init__(self, username, password='12345', start_date='2021-05-19', expiry_date='2031-05-19'):
        self.username = username
        self.password = password
        self.start_date = start_date
        self.expiry_date = expiry_date
        self._read = []

    def read_article(self, article):
        self._read.append(article)
        return article.article_id


repository.py
=================================================
# Software Architecture and Design Patterns -- Lab 3 starter code
# An implementation of the Repository Pattern
# Copyright (C) 2021 Hui Lan

import abc
import model
from sqlalchemy.orm.exc import NoResultFound


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError


class ArticleRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, article):
        self.session.add(article)

    def get(self, reference):
        try:
            return self.session.query(model.Article).filter_by(article_id=reference).one()
        except NoResultFound:
            return None

    def list(self):
        return self.session.query(model.Article).all()


class UserRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user):
        self.session.add(user)

    def get(self, reference):
        try:
            return self.session.query(model.User).filter_by(username=reference).one()
        except NoResultFound:
            return None

    def list(self):
        return self.session.query(model.User).all()


services.py
=================================================
# Software Architecture and Design Patterns -- Lab 3 starter code
# An implementation of the Service Layer
# Copyright (C) 2021 Hui Lan

# word and its difficulty level
WORD_DIFFICULTY_LEVEL = {'starbucks':5, 'luckin':4, 'secondcup':4, 'costa':3, 'timhortons':3, 'frappuccino':6}

import pytest
import math
import model

class UnknownUser(Exception):
    pass

class NoArticleMatched(Exception):
    pass

def read(user, user_repo, article_repo, session):
    u = user_repo.get(user.username)
    if u == None or u.password != user.password:
        raise UnknownUser()

    articles = article_repo.list()
    
    if articles == None:
        raise NoArticleMatched()
        
    words = session.execute(
        'SELECT word FROM newwords WHERE username=:username',
        dict(username=user.username),
    )

    sum = 0
    count = 0
    for word in words:
        sum += WORD_DIFFICULTY_LEVEL[word[0]]
        count += 1
    
    if count == 0:
        count = 1

    average = round(sum / count) + 1
    if average < 3:
        average = 3
    
    for article in articles:
        if average == article.level:
            article_id = user.read_article(article)
            session.add(model.Reading(username = user.username, article_id = article_id))
            session.commit()
            return article_id
        
    raise NoArticleMatched()


conftest.py
=================================================
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


test_services.py
=================================================
# Software Architecture and Design Patterns -- Lab 3 starter code
# Run this script using the following command: pytest -v -s test_services.py
# Copyright (C) 2021 Hui Lan

import pytest

import model
import repository
import services

@pytest.mark.usefixtures('prepare_data')
def test_read_article_level4(get_session):
    session = get_session()
    article_repo = repository.ArticleRepository(session)
    user_repo = repository.UserRepository(session)

    username = 'mrlan'
    password = '12345'
    user = model.User(username=username, password=password)
    article_id = services.read(user, user_repo, article_repo, session)

    result = session.execute(
        'SELECT article_id FROM readings WHERE username=:username',
        dict(username=username),
    )

    lst = [r[0] for r in result]

    assert article_id == 2
    assert lst[0] == 2



@pytest.mark.usefixtures('prepare_data')
def test_read_article_level5(get_session):
    session = get_session()
    article_repo = repository.ArticleRepository(session)
    user_repo = repository.UserRepository(session)

    username = 'lanhui'
    password = 'Hard2Guess!'
    user = model.User(username=username, password=password)
    article_id = services.read(user, user_repo, article_repo, session)

    result = session.execute(
        'SELECT article_id FROM readings WHERE username=:username',
        dict(username=username),
    )

    lst = [r[0] for r in result]
    assert article_id == 1
    assert lst[0] == 1



@pytest.mark.usefixtures('prepare_data')
def test_read_article_level6(get_session):
    session = get_session()
    article_repo = repository.ArticleRepository(session)
    user_repo = repository.UserRepository(session)

    username = 'hui'
    password = 'G00d@English:)'
    user = model.User(username=username, password=password)
    with pytest.raises(services.NoArticleMatched):
        article_id = services.read(user, user_repo, article_repo, session)



@pytest.mark.usefixtures('prepare_data')
def test_user_with_wrong_password(get_session):
    session = get_session()
    article_repo = repository.ArticleRepository(session)
    user_repo = repository.UserRepository(session)

    username = 'mrlan'
    password = '54321'
    user = model.User(username=username, password=password)
    with pytest.raises(services.UnknownUser):
        article_id = services.read(user, user_repo, article_repo, session)



@pytest.mark.usefixtures('prepare_data')
def test_user_with_wrong_username(get_session):
    session = get_session()
    article_repo = repository.ArticleRepository(session)
    user_repo = repository.UserRepository(session)

    username = 'MrLan'
    password = '12345'
    user = model.User(username=username, password=password)
    with pytest.raises(services.UnknownUser):
        article_id = services.read(user, user_repo, article_repo, session)



=================================================

首先初始化用户和文章库，然后创建实体用户，调用服务的read()函数来获取article_id，最后，断言比较;

但是第三个函数test_read_article_level6()是特殊的，因为在数据库中没有关于level6的文章，所以它需要输出异常- NoArticleMatched();

通过services.py和test_services.py两个文件，在数据库中搜索所有用户，来验证用户是否存在，如果不存在，则输出异常- UnknownUser();

单一职责原则，简称SRP，定义是：有且仅有一个原因引起接口或类的变更。

read()函数遵循SRP单一职责原则。因为函数只用于返回article_id，如果没有article_id，则输出异常。



