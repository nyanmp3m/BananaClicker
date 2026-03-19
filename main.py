#!/usr/bin/env venv/bin/python

from flask import Flask, render_template
from SQLdata import db_session

app = Flask(__name__)


@app.route('/')
def index():
    db_session.global_init("db/users.db")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
