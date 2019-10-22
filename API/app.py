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

# # Load pickled model and pickled vectors template
# nn = load('nearestneighbor_smaller.joblib')
# tfidf = load('tfidf (1).joblib')


# def get_books(description):
#     '''Predicts books that fit a given description
#      and outputs a list with the 5 best'''
#     post = tfidf.transform([description])
#     post = bsr_matrix.todense(post)
#     pred_array = nn.kneighbors(post)
#     output = []
#     for pred in pred_array[1][0]:
#         book = DB.session.query(
#             Book.title, Book.author, Book.rating, Book.isbn
#             ).filter(Book.id == int(pred)).all()[0]
#         output.append(book)
#     return output


class Comments(DB.Model):
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
    subscribers = DB.Column(DB.Integer(8))


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


# API route Comments
@app.route('/api/comments', methods=['POST'])
def commentsAPI():
    TODO  # API here


@app.route('/api/subreddits', methods=['POST'])
def subredditsAPI():
    TODO  # API here


if __name__ == '__main__':
    app.run(debug=True)