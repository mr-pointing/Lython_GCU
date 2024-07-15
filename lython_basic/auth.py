# -------- R. Pointing
# -------- GCU Final Project
# -------- Authorization file, stores the login and logout methods
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from lython_basic.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Creates a new user
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            existing_user = db.execute("SELECT id FROM user WHERE username = ?", (username, )).fetchone()

            if existing_user:
                error = 'Username already exists.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = 'Username already exists.'
            else:
                return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')

# Login form
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Invalid Username'
        elif not check_password_hash(user['password'], password):
            error = 'Invalid password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

# Checks to see if there is a session id active otherwise user is None
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# Logout the user
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Checks if a user is loaded and redirects to the login page otherwise
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
