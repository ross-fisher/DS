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


# find the top subreddits, currently top 5
top_subreddits = list(reddit.subreddits.popular())[0:200]
top_subreddits = [s.display_name for s in top_subreddits]
print(top_subreddits)


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


# get info on top subreddits
top_sub_info = subreddit_info(top_subreddits)
# print(top_sub_info)
# conver to csv
top_sub_info.to_csv('top_subreddit_info.csv')


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
# print(sample_comments(subreddit))
