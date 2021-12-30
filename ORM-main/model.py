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






