import src.prawapi as prawapi
from src.util import *
import praw
import pandas as pd
from flask import Flask, request, json
from sqlalchemy import create_engine
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

def get_subreddit(title):
    '''Predicts subreddit that fits a given title
     and outputs a list with the 5 best'''
    # Load Model
    model = load('nn.joblib')
    tfidf = load('tfvect.joblib')
    post = tfidf.transform([title])
    pred_array = model.kneighbors(post)
    output = []
    # pred # subreddit_name 
    top_5_subreddit_scores = pred_array[0][0:5][0]
    top_5_subreddit_indices = pred_array[1][0:5][0]

    names = []
    conn = db.connect()
    for sr_index in top_5_subreddit_indices:
        result = None
        try:
            # index has to be wrapped like ("index") because it's a reserved sql keyword
            recommendation = conn.execute(f'select subreddit_name from submissions where ("index") = {sr_index};').fetchone()
            names.append(recommendation[0])
        except Exception as e:
            print(f'SQL Error: {e}')

    conn.close()
    return names

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

@app.route('/submission_analysis', methods=['GET', 'POST'])
def submission_analysis():
    """Send a post request to this url to receive the model's prediction."""
    if request.method == 'POST':
        submission_text = request.data
        data = request.get_json(force=True)

#        data['tokens'] = tokenize(data['title'] + data['post'])
        #data['tokens'] = tokenize(data['content'])
        x = get_subreddit( data['title'] + data['post'] )
        return jsonify(x)

if __name__ == "__main__":
    app.run(debug=True)
