import requests
import json
from requests_oauthlib import OAuth1

STREAM_FILTER_STATUSES = 'https://stream.twitter.com/1.1/statuses/filter.json'

class TwitterApi:
	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

	def on_status_change(self, userId, process):
		params = {
			# 'follow':'2449437698'
			'follow': userId
		}
		url = STREAM_FILTER_STATUSES

		response = requests.get(url, auth = self.auth, params = params, stream = True)

		for line in response.iter_lines():
			if line:
				print(line)
				jsonifiedResponse = json.loads(line)
				if jsonifiedResponse["user"]["id_str"] == userId:
					tweet = Tweet(jsonifiedResponse["text"])
					process(tweet)

class Tweet:
	def __init__(self, text):
		self.text = text
