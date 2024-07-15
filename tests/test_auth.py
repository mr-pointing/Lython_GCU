# -------- R. Pointing
# -------- GCU Final Project
# -------- Testing authentication

import pytest
from flask import g, session
from lython_basic.db import get_db

def test_register(client, app):

    # Testing a get request (specifically using code 200 to test render)
    assert client.get('/auth/register').status_code == 200

    # Testing a post request
    response = client.post(
        '/auth/register', data={'username': 'abc', 'password': 'abc'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'abc'",
        ).fetchone() is not None

# Tells Pytest to run the same test function with different args
@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('abc', '', b'Password is required.'),
        ('test', 'test', b'Username already exists.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('abc', 'test', b'Invalid Username'),
        ('test', 'abc', b'Invalid password')
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
