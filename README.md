4/21/24

# Lython

Lython is a chatbot-based platform using Open AI's API and Langchain to help students learn Python
and get help directly with the questions they have for class and homework.

I wanted to make this application based off of my experience as a teacher who has 
high school students trying to learn Python. I often don't have time in one class period
to reach everyone, and thought that this might be a good alternative to having them 
use regular Chat-GPT, which would just give them answers. 

## Installation

From a virtual environment, run the following commands;

```bash
pip install -i https://test.pypi.org/simple/ lython==1.0.1

pip install openai

flask --app lython init-db

flask --app lython run 
```

You can then visit the link it provides you, or http://127.0.0.1:5000/auth/register to start

# Dependencies

The application is built primarily using [Flask](https://flask.palletsprojects.com/en/3.0.x/). HTML and CSS structured
mostly from their documentation, with a little customization to fit the school colors/theme.

Database for the Users and Chat Responses stored using a [SQLite](https://www.sqlite.org/) Database.

Calls to the chatbot for general chat are using [OpenAI's](https://platform.openai.com/docs/introduction) API.

My students use two platforms primarily for work; [Coding Bat](https://codingbat.com) and Amazon's
[Project STEM](https://projectstem.org). Since Project STEM requires an account to view, and I wanted
to show off the webscraping ability via [LangChain](https://python.langchain.com/docs/get_started/introduction), I
decided to just include problems from Coding Bat.

The project has been uploaded to [Pythons Test Package Deployment](https://test.pypi.org/project/lython/), 
and is the current main distribution method.

## Usage

After the database is set up, you must configure an Open AI key to a global environment variable, "OPENAI-API-KEY".

You can begin by registering for an account. Questions are unable to be asked until a user has signed in.

The current Coding Bat questions are saved in "codingbat_urls.csv", so any more questions you want to add from there, you
can drop the URL in there. You can begin asking for question specific questions in the RAG chat.


## Acknowledgements
This project was inspired by my students, and their constant need to cheat on homework assignments.

Big thank you for Blake (Blaque2Pi), Benjamin, and a few other GCU students for reviewing my code, help, and advice over the last 
few months.


## License

[MIT](https://choosealicense.com/licenses/mit/)




