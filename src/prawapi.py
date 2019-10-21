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

<<<<<<< Updated upstream
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
=======
# test
print(reddit.read_only)

# test for posts in a subreddit
# for submission in reddit.subreddit('redditdev').hot(limit=10):
#     print(submission.title)

subreddit = reddit.subreddit('subreddits')

# test for top subreddits
# for submission in subreddit.top(limit=20):
#     print(submission.title)
#     print(submission.score)
#     print(submission.id)
#     print(submission.url)

# find the popular subreddits, currently top 5
top_subreddits = list(reddit.subreddits.popular())[0:5]
top_subreddits = [s.display_name for s in top_subreddits]
print(top_subreddits)

# print(reddit.subreddit('redditdev').description)
# print(reddit.subreddit('redditdev').subscribers)
>>>>>>> Stashed changes


def subreddit_info(subreddits):
    rows = []
    for x in range(len(top_subreddits)):
        rpath = reddit.subreddit((top_subreddits[x]))
        rows.append(
            dict(
                subreddit_name=top_subreddits[x],
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
<<<<<<< Updated upstream
    comments = list(sr.comments(limit=n)) # TODO check if this sample is fair
=======
    comments = list(sr.comments())[0:n]  # TODO check if this sample is fair
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
subreddit = reddit.subreddit('learnpython')
=======
subreddit = reddit.subreddit('python')
>>>>>>> Stashed changes
print(sample_comments(subreddit))
