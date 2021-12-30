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
