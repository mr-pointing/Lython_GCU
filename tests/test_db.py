# -------- R. Pointing
# -------- GCU Final Project
# -------- Testing database file

import sqlite3
import pytest
from lython_basic.db import get_db

# Testing that the database can be opened and closed without issue
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

# Testing the init-db command and the init_db function
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('lython_basic.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output
    assert Recorder.called
