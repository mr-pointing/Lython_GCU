# -------- R. Pointing
# -------- GCU Final Project
# -------- Chat file, stores the functions for OpenAI and the main page

from flask import (
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)
import openai
import datetime
from werkzeug.exceptions import abort
from lython.auth import login_required
from lython.db import get_db

bp = Blueprint('chat', __name__)


openai.api_key = 'OPEN-AI-API-KEY'
temp = 0.3
max_t = 1000
model_type = "gpt-3.5-turbo"

def ask_python_question(text):
    prompt = get_prompt_python() + text
    response = openai.chat.completions.create(
        model=model_type,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_t,
        temperature=temp,
        n=1
    )
    content = response.choices[0].message.content

    return content


def get_prompt_python():
    return '''Please answer my question while trying to teach me about one of the core fundamental concepts of 
        programming (variables, conditionals, loops, data structures, syntax, or debugging), ONLY in the 
        language Python in under 200 words. 

        If there is nothing wrong, tell me so.

        Tell me what kind of problem I am having, and help me understand without explaining any code to me. 
        If you're going to use any code examples, please use different variable names, and under no circumstances should you
        give me the answer. After explaining my problem, demonstrate how to properly use the advice given.
        
        Also, before each snippet of code, put <pre><code> before it and </code></pre> after.

        My Question:

        '''

@bp.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    error = None
    bot_response = ''
    if g.user is not None:
        name = g.user['username']
    else:
        name = ''

    if request.method == 'POST':
        user_question = request.form['user_question']


        if not user_question:
            error = "Need to ask a question first."
        else:
            bot_response = ask_python_question(user_question)

        if not name:
            error = "Need to log-in first."

        if error is None and name:
            try:
                # For whatever reason, using response_timestamp causes an error
                # when trying to display all responses, so for now leaving this out
                # response_timestamp = datetime.datetime.now().isoformat()
                db.execute(
                    "INSERT INTO ChatResponses(user_id, input_prompt, response_text,"
                    "model_used, temperature, max_tokens) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (session['user_id'], user_question, bot_response,
                     model_type, temp, max_t),
                )
                db.commit()
            except Exception as e:
                error = str(e)
        else:
            flash(error)

    return render_template('chat/index.html', name=name, bot_response=bot_response)

# Function to collect all chat history
def get_chat_history(user_id):
    db = get_db()
    chat_history = db.execute(
        'SELECT input_prompt, response_text'
        ' FROM ChatResponses WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    return chat_history

@bp.route('/history')
def history():
    if g.user is not None:
        user_id = g.user['id']
        chat_history = get_chat_history(user_id)
        return render_template('chat/history.html', chat_history=chat_history)
    else:
        flash('You need to login to view chat history.')
        return redirect(url_for('auth.login'))