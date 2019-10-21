# import important libraries
import praw
import configparser

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


# print(reddit.subreddit('redditdev').description)
# print(reddit.subreddit('redditdev').subscribers)
