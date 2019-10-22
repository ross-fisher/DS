import praw
import configparser
import pandas as pd
from flask import Flask, request
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from decouple import config
from scipy.sparse import bsr_matrix
from joblib import load

# config('DATABASE_URL')
app = Flask(__name__)
db = create_engine('sqlite:///database.db')
conn = db.connect()


class Subreddit(Resource):
    def get(self, subreddit_name):
        query = conn.execute(
            f'select * from subreddit where subreddit_name = {subreddit_name}'
            )
        print(query.cursor.fetchone())
        return query.cursor.fetchone()

    def put(self, todo_id):
        request.form['data']
        pass


def update_subreddit_table():
    conn.execute("""
        insert into subreddit (name) values 'learnpython';
    """)
    pass


def create_tables():
    conn.execute("""create table subreddit (
        id INTEGER PRIMARY KEY,
        name TEXT
    )""")


create_tables()
update_subreddit_table()
api.add_resource(Subreddit, '/subreddit')

# grab userdata from hidden files
config = configparser.ConfigParser()
config.read('secrets.ini')
user_agent = config.get('reddit', 'user_agent')
client_id = config.get('reddit', 'client_id')
client_secret = config.get('reddit', 'client_secret')
password = config.get('reddit', 'password')
username = config.get('reddit', 'username')

# get api access token
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)


@app.route('/')
def root():
    return 'Hello'
