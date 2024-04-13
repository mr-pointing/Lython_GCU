# -------- R. Pointing
# -------- GCU Final Project
# -------- Configure Test file: sets up the testing environment
import os
import tempfile
import pytest
from lython import create_app
from lython.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')

# A class that takes care of logging in and logging out
class AuthActions(object):
    def __init__(self, client):
        self.client = client

    def login(self, username='test', password='test'):
        return self.client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.client.get('/auth/logout')


@pytest.fixture
def app():
    # tempfile.mkstemp() creates a temporary file, and returns the file descriptor and path
    db_fd, db_path = tempfile.mkstemp()

    # TESTING set to True so the app knows, DATABASE path overridden to not affect instance
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Creates the database and inserts the test variables into it
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app
    os.close(db_fd)
    os.unlink(db_path)

# app.test_client() is called so the client can make requests without the use of a server
@pytest.fixture
def client(app):
    return app.test_client()

# app.test_cli_runner() is called so click commands can be registered
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# auth() calls AuthActions and passes the current testing client
@pytest.fixture
def auth(client):
    return AuthActions(client)