#!/usr/bin/env venv/bin/python

from flask import Flask, render_template
from first_DB.users_data import db_session

app = Flask(__name__)

db_session.global_init("first_DB/db/users.db")

@app.route('/')
def index():
    db_sess = db_session.create_session()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
