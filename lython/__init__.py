# -------- R. Pointing
# -------- GCU Final Project
# -------- __init__ file, stores the application factory
import os
from flask import Flask

def create_app(test_config=None):

    # Creating and configuring app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lython.sqlite')
    )

    if test_config is None:
        # Load the instance config, if exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')

    return app