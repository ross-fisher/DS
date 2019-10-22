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
import src.prawapi as prawapi

# config('DATABASE_URL')
app = Flask(__name__)
db = create_engine('sqlite:///database.db')
api = Api(app)


class Subreddit(Resource):
    def get(self, subreddit_name):
        conn = db.connect()
        query = conn.execute(
            f"select * from subreddit where name = '{subreddit_name}';"
            )

        return query.cursor.fetchone()

    def put(self, todo_id):
        conn = db.connect()
        request.form['data']
        pass


class Subreddits(Resource):
    def get(self, page_number):
        pass


def update_subreddit_table():
    conn = db.connect()
    conn.execute("""
        insert into subreddit (name) values ('learnpython');
    """)
    pass


def create_tables():
    top_df = prawapi.top_submissions()
    top_df.to_sql('submissions', con=db, if_exists='replace')

    print(db.execute('select name from submissions;').fetchone())


create_tables()
# update_subreddit_table()
# api.add_resource(Subreddit, '/r/<subreddit_name>')

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
