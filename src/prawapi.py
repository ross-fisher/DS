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


top_subreddits = list(reddit.subreddit.popular())[0:5]


# for updating the sql database
def get_top_subreddits_table(reddit, n=50):
    popular_subreddits = reddit.subreddits.popular()[0:n]
    subreddit_infos = []
    for sr in popular_subreddits:
        subreddit_infos += [dict(
            id=sr.id,
            name=sr['display_name']
        )]
    df = pd.DataFrame(subreddit_infos)


# get subreddit info
def subreddit_info(subreddits):
    rows = []
    for x in range(len(subreddits)):
        rpath = reddit.subreddit((subreddits[x]))
        rows.append(
            dict(
                subreddit_name=subreddits[x],
                subreddit_description=rpath.description,
                subreddit_id=rpath.id,
                subreddit_nsfw=rpath.over18,
                subreddit_subscribers=rpath.subscribers
            )
        )
    subreddit_info = pd.DataFrame(rows)
    return subreddit_info


print(subreddit_info(top_subreddits))


def sample_comments(sr, n=20):
    rows = []
    comments = list(sr.comments(limit=n))  # TODO check if this sample is fair
    for comment in comments:
        rows.append(
            dict(body=comment.body,
                 body_html=comment.body_html,
                 id=comment.id,
                 author_id=comment.author.id,
                 subreddit_id=sr.id,
                 created_utc=comment.created_utc))
    df = pd.DataFrame(rows)
    return df


subreddit = reddit.subreddit('learnpython')
print(sample_comments(subreddit))
