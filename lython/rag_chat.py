# -------- R. Pointing
# -------- GCU Final Project
# -------- Rag_Chat file, stores the functions for specifically RAG related chat features

from flask import (
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)
from lython.db import get_db
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_openai import ChatOpenAI
from langchain.chains import (
    RetrievalQAWithSourcesChain, SequentialChain, LLMChain
)
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

import os
import pandas as pd

bp = Blueprint('rag_chat', __name__)


# Settings for OpenAI
ChatOpenAI.api_key = os.getenv('OPENAI_API_KEY')
temp = 0.0001
max_t = 1000
model_type = "gpt-3.5-turbo"

# Creating the LLM, splitter, and embeddings
llm = ChatOpenAI(temperature=temp, max_tokens=max_t)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=0
)
embeddings = OpenAIEmbeddings()

# Opening the Coding Bat problems, splitting them, and indexing them
csv_path = os.path.join(os.path.dirname(__file__), 'codingbat_urls.csv')
cb_urls = list(pd.read_csv(csv_path))
cb_loader = UnstructuredURLLoader(urls=cb_urls)
cb_data = cb_loader.load()
cb_chunks = splitter.split_documents(cb_data)
cb_index = FAISS.from_documents(cb_chunks, embeddings)

# Chain to call questions with sources
cb_chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=cb_index.as_retriever())

# Creating prompt template to send in info about question asked to provide a start
rag_pt = PromptTemplate(
    input_variables = ['answer'],
    template = """Given the information {answer}, help the user get a start on their question. 
     
     If the source info returns some instructions, give me some advice on what concepts I should know, and write some
     very basic sample code to help me start, no
     more than 5 lines of code.   
     
     
     If the source info is just, "I don't know", ask the user to provide a specific 
    question to get help with.
    
    
    """
)
rag_chain = LLMChain(llm = llm, prompt = rag_pt)

# Combined sequential chain
combined_chain = SequentialChain(
    chains = [cb_chain, rag_chain],
    input_variables = ['question']
)

@bp.route('/rag_chat', methods=['GET', 'POST'])
def rag_chat():
    db = get_db()
    error = None
    rag_response = ''
    if g.user is not None:
        name = g.user['username']
    else:
        name = ''

    if request.method == 'POST':
        user_rag_question = request.form['user_rag_question']

        if not user_rag_question:
            error = "Need to ask a question first."
        else:
            rag_response = combined_chain.invoke({"question": user_rag_question}, return_only_outputs=True)

        if not name:
            error = "Need to log-in first."

        if error is None and name:
            try:
                db.execute(
                    "INSERT INTO ChatResponses(user_id, input_prompt, response_text,"
                    "model_used, temperature, max_tokens)"
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (session['user_id'], user_rag_question, rag_response['text'],
                     model_type, temp, max_t),
                )
                db.commit()
            except Exception as e:
                error = str(e)
        else:
            flash(error)
    if rag_response:
        return render_template('rag_chat/rag_chat.html', name=name, rag_response=rag_response['text'])
    else:
        return render_template('rag_chat/rag_chat.html', name=name, rag_response=rag_response)