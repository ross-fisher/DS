import src.prawapi as prawapi
from src.util import *
import praw
import pandas as pd
from flask import Flask, request, json
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from decouple import config
from scipy.sparse import bsr_matrix
from joblib import load
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import joblib
from joblib import load

# config('DATABASE_URL')
app = Flask(__name__)
db = create_engine('sqlite:///database.db')

# Load Model
model = load('reddit.joblib')
tfidf = load('tfidf.joblib')


def get_subreddit(title):
    '''Predicts subreddit that fits a given title
     and outputs a list with the 5 best'''
    post = tfidf.transform([title])
    pred_array = model.kneighbors(post)
    output = []
    for pred in pred_array[1][0]:
        subreddit = db.session.query(
            Subreddit.title, Subreddit.name, Subreddit.score
            ).filter(Subreddit.id == int(pred)).all()[0]
        output.append(subreddit)
    return output

# model = joblib.load('reddit_model')


def update_tables():
    # find top subreddits
    top_subs = prawapi.top_subreddits(top_x=200)
    # find info on top subreddits
    top_sub_info = prawapi.subreddit_info(top_subs)
    # find info on top submissions of top subreddits
    top_submission = prawapi.top_submissions(subreddit=top_subs, top_x=25)
    # create and populate SQL tables with the info
    top_sub_info.to_sql('subreddit', con=db, if_exists='replace')
    top_submission.to_sql('submissions', con=db, if_exists='replace')
    top_sub_info.to_csv('top_subreddit_info.csv')
    top_submission.to_csv('top_submission_info.csv')


# grab userdata from hidden files
# config = configparser.ConfigParser()
# config.read('secrets.ini')

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
    return """
        <h1>Post Here Reddit Predictor API</h1>

        <div>
            <h4>From command line</h4>
            curl -H "Content-type: application/json" -d '{
                "content" : "blah blah blah",
                 "title" : "The title of my submission"
                }' -X POST
                https://post-here-reddit-predictor-api.herokuapp.com/submission_analysis
        </div>

        <div>Full application at <a href=""></a>.
         Github at <a href="http://https://github.com/Build-Week-Post-Here/DS">
         http://https://github.com/Build-Week-Post-Here/DS</a> </div>
    """


@app.route('/refresh')
def refresh():
    update_tables()
    return 'Data Refreshed'

# for reference
# @app.route('/messages', methods=['POST'])
# def api_message():
#     if request.headers['Content-Type'] == 'text/plain':
#         return "Text Message: " + request.data
#     elif request.headers['Content-Type'] == 'application/json':
#         return "JSON Message: " + json.dumps(request.json)
#     elif request.headers['Content-Type'] == 'application/octet-stream':
#         f = open('./binary', 'wb')
#         f.write(request.data)
#         f.close()
#         return "Binary message written!"
#     else:
#         return "415 Unsupported Media Type ;)"


@app.route('/submission_analysis', methods=['GET', 'POST'])
def submission_analysis():
    """Send a post request to this url to receive the model's prediction."""
    if request.method == 'POST':
        submission_text = request.data
        data = request.get_json(force=True)
        # content and title?
        columns = [data['subreddit_name'], data['title']]
        return jsonify(columns)
        # data['tokens'] = data['title'].apply(tokenize)
        # tfidf = TfidfVectorizer(
        #     tokenizer=tokenize, min_df=0.1, max_df=0.9, ngram_range=(1, 2)
        #     )
        # sparse = tfidf.fit_transform(data['title'])
        # dtm = pd.DataFrame(
        #     sparse.todense(), columns=tfidf.get_feature_names()
        # )


if __name__ == "__main__":
    app.run(debug=True)
