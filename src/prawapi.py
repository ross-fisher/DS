# import important libraries
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


# find the top x subreddits, defualt 100
def top_subreddits(top_x=100):
    top_subs = list(reddit.subreddits.popular())[0:top_x]
    top_subs = [s.display_name for s in top_subs]
    return top_subs


# get subreddit info
def subreddit_info(subreddits):
    rows = []
    for x in range(len(subreddits)):
        rpath = reddit.subreddit((subreddits[x]))
        rows.append(
            dict(
                # subreddit names
                subreddit_name=subreddits[x],
                # subreddit descriptions
                subreddit_description=rpath.description,
                # subreddit reddit id
                subreddit_id=rpath.id,
                # subreddit nsfw tag
                subreddit_nsfw=rpath.over18,
                # subreddit subscriber count
                subreddit_subscribers=rpath.subscribers
            )
        )
    # convert the dictionary to dataframe
    subreddit_info = pd.DataFrame(rows)
    # return the info
    return subreddit_info


def make_comments_table(comments):
    rows = []
    for comment in comments:
        rows.append(
            dict(body=comment.body,
                 id=comment.id,
                 author_id=comment.author.id,
                 subreddit_id=comment.subreddit_id,
                 created_utc=comment.created_utc))
    df = pd.DataFrame(rows)
    return df


def test():
    # get test subreddits
    sr = reddit.subreddit('learnpython')
    # get test comments
    comments = list(sr.comments(limit=10))  # TODO check if this sample is fair
    # get comments table
    comment_table = make_comments_table(comments)
    # get top subreddits, currently 10
    top_subs = top_subreddits(10)
    # print comment table
    print(comment_table)
    # get info on top subreddits
    top_sub_info = subreddit_info(top_subs)
    print(top_sub_info)
    # convert to csv
    top_sub_info.to_csv('top_subreddit_info.csv')


# run the test function
test()
