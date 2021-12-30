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
