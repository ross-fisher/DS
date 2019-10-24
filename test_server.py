import requests
URL='https://post-here-reddit-ranker-api.herokuapp.com/submission_analysis'
params = {'content' : 'something aoetnuhntaoeh aoetnuh'}

r = requests.post(url = URL, data = params)

#data = r.json()
#print(data)
print(r)
