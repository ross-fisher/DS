from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from scipy.sparse import bsr_matrix
from joblib import load

# config('DATABASE_URL')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///the_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)
# temp
class Comment(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    subbredditKey = DB.Column(
        DB.Integer, DB.ForeignKey('subreddit.id'), nullable=False
        )
    body = DB.Column(DB.String(25000))
    commentID = DB.Column(DB.Text)
    authorID = DB.Column(DB.Text)
    subredditID = DB.Column(DB.Text)
    createdUTC = DB.Column(DB.Text)


class Subreddit(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Text)
    description = DB.Column(DB.Text)
    subredditID = DB.Column(DB.Text)
    nsfw = DB.Column(DB.Boolean)
    subscribers = DB.Column(DB.Integer)

DB.drop_all()
DB.create_all()

import praw
import configparser
import pandas as pd

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

def update_subreddit_table(subreddits):
    try:  # try doesn't actually work
        for subreddit in subreddits:
            print('THNHAOETUHNSAOEUHTNSAOEUHTNH')
            sr = Subreddit(
                name=subreddit.display_name, 
                description=subreddit.description,
                subredditID = subreddit.id,
                nsfw = subreddit.over18,
                subscribers = subreddit.subscribers
            )
            print("display name", subreddit.display_name)
            print("descritpion", subreddit.description)
            print("id", subreddit.id)
            print("over18", subreddit.over18)
            print("subscribers", subreddit.subscribers)
            #print(Subreddit.query.filter_by(subredditID=subreddit.id))
            DB.session.add(sr)
        print("hello")
        DB.session.commit()
        print("hello2")
        #print(Subreddit.query.all())
        return 'okay'
    except Exception as e:
        return f'Error {e}'
    return 'Okay'

def update_user_table(users):
    pass

def update_comments_table(comments):
    try: 
        for comment in comments:
            c = Comment(body=comment.body,
                comment_id=comment.id,
                author_id=comment.author.id,
                subreddit_id=comment.subreddit_id,
                created_utc=comment.created_utc)
            DB.session.add(c)
        DB.session.commit()
    except Exception as e:
        print(f'Error {e}')

 def update_submissions_table(submission):
    try: 
        for submission in submission:
            c = Comment(name=submission.name,
                submission_id=submission.id,
                author_id=submission.author.id,
                body=submission.selftext or "",
                url=submission.url,
                num_comments=submission.num_comments,
                score=submission.score,
                subreddit_name=submission.subreddit,
                created_utc=submission.created_utc)
            DB.session.add(c)
        DB.session.commit()
    except Exception as e:
        print(f'Error {e}')   

@app.route('/update_tables')
def update_all_tables():
    DB.drop_all()
    top_subreddits = get_top_subreddits(n=5)
    update_subreddit_table(top_subreddits)
    return 'okay'

# find the top x subreddits, defualt 100
def get_top_subreddits(n=100):
    top_subs = list(reddit.subreddits.popular())[0:n]
    return top_subs

def test():
    top_subreddits = get_top_subreddits(n=5)
    update_subreddit_table(top_subreddits)


@app.route('/')
def root():
    return 'Hello'


# API route Comments
@app.route('/api/comments', methods=['POST'])
def commentsAPI():
    pass  # API here


@app.route('/api/subreddits', methods=['POST'])
def subredditsAPI():
    pass  # API here



# # class Template
# class Book(DB.Model):
#     id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
#     webpage = DB.Column(DB.BigInteger)
#     title = DB.Column(DB.String(300))
#     author = DB.Column(DB.String(100))
#     descrip = DB.Column(DB.String(25000))
#     rating = DB.Column(DB.Float)
#     num_ratings = DB.Column(DB.String(30))
#     num_reviews = DB.Column(DB.String(30))
#     isbn = DB.Column(DB.String(110))
#     isbn13 = DB.Column(DB.String(110))
#     binding = DB.Column(DB.String(100))
#     edition = DB.Column(DB.String(125))
#     num_pages = DB.Column(DB.String(100))
#     published_on = DB.Column(DB.String(150))
#     genres = DB.Column(DB.String(300))

#     def __repr__(self):
#         return f'Book: {self.title} writtien by {self.author}'


# # API route template
# @app.route('/api/description', methods=['POST'])
# def api():
#     description = request.get_json('description')['description']
#     output = get_books(description)
#     return jsonify(output)