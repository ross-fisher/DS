# import important functions
import requests
import requests.auth

# Requesting token from OAuth2/reddit.com
client_auth = requests.auth.HTTPBasicAuth(
    'H-rICgMVKGTHQQ', 'LvnlKL_Jj7ndtNHHmSvPZDbmEKY'
    )
post_data = {
    'grant_type': 'password',
    'username': 'BWPostHere',
    'password': 'Passlock1'
    }
headers = {'User-Agent': 'BWPostHere/0.1 by u/BWPostHere'}
response = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    auth=client_auth,
    data=post_data,
    headers=headers
    )
response.json()
