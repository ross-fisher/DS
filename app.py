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


def create_tables():
    # find top subreddits
    top_subs = prawapi.top_subreddits(top_x=100)
    # find info on top subreddits
    top_sub_info = prawapi.subreddit_info(top_subs)
    # find info on top submissions of top subreddits
    top_submission = prawapi.top_submissions(subreddit=top_subs, top_x=10)
    # create and populate SQL tables with the info
    top_sub_info.to_sql('subreddit', con=db, if_exists='replace')
    top_submission.to_sql('submissions', con=db, if_exists='replace')


# create_tables()
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


@app.route('/refresh')
def refresh():
    create_tables()
    return 'Data Refreshed'


@app.route('/submission_analysis', methods=['POST'])
def submission_analysis(submission_text=''):
    # model here
    return submission_text  # suggested subreddit
