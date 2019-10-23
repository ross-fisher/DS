import praw
import configparser
import pandas as pd
from flask import Flask, request, json
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from decouple import config
from scipy.sparse import bsr_matrix
from joblib import load
import joblib
import src.prawapi as prawapi

# config('DATABASE_URL')
app = Flask(__name__)
db = create_engine('sqlite:///database.db')

# Load Model
# model = joblib.load('reddit_model')

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
#config = configparser.ConfigParser()
#config.read('secrets.ini')
user_agent = config('user_agent')
client_id = config('client_id')
client_secret = config('client_secret')
password = config('password')
username = config('username')

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


@app.route('/messages', methods=['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"

# curl -H "Content-type: text/plain" -d "something"  -X POST the url
# Content-type: application/json
@app.route('/submission_analysis', methods=['GET', 'POST'])
def submission_analysis():
    if request.method == 'POST':
        submission_text = request.data
        return submission_text
