# -------- R. Pointing
# -------- GCU Final Project
# -------- Testing factory file
from lython_basic import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
