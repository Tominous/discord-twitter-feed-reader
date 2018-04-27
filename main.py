import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from twitter.twitter_wrapper import TwitterApi
from discord.discord_wrapper import DiscordApi

class ACTask:
	account_id = os.environ.get('TWITTER_ACCOUNT_ID')
	web_hook = os.environ.get('DISCORD_WEBHOOK')

	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.twitter = TwitterApi(consumer_key, consumer_secret, access_token, access_secret)
		self.discord = DiscordApi(self.web_hook)

	def handle_tweet(self, tweet):
		self.discord.send_discord_message(tweet.text)

	def execute(self):
		print("Starting up ACTask....")
		self.twitter.on_status_change(self.account_id, self.handle_tweet)


class BCJPTask:

	account_id = os.environ.get('BCJP_ACCOUNT_ID')
	web_hook = os.environ.get('BATTLECAT_WEBHOOK')

	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.twitter = TwitterApi(consumer_key, consumer_secret, access_token, access_secret)
		self.discord = DiscordApi(self.web_hook)

	def handle_tweet(self, tweet):
		message = '[BCJP]\n'+tweet.text
		self.discord.send_discord_message(message)

	def execute(self):
		print("Starting up BCJPTask....")
		self.twitter.on_status_change(self.account_id, self.handle_tweet)

class BCENTask:
	account_id = os.environ.get('BCEN_ACCOUNT_ID')
	web_hook = os.environ.get('BATTLECAT_WEBHOOK')

	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.twitter = TwitterApi(consumer_key, consumer_secret, access_token, access_secret)
		self.discord = DiscordApi(self.web_hook)

	def handle_tweet(self, tweet):
		message = '[BCEN]\n'+tweet.text
		self.discord.send_discord_message(message)

	def execute(self):
		print("Starting up BCENTask....")
		self.twitter.on_status_change(self.account_id, self.handle_tweet)

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret = os.environ.get('ACCESS_TOKEN_SECRET')

bcjp_task = BCJPTask(consumer_key, consumer_secret, access_token, access_secret)
bcen_task = BCENTask(consumer_key, consumer_secret, access_token, access_secret)
ac_task = ACTask(consumer_key, consumer_secret, access_token, access_secret)

print("Script started.")
executor = ThreadPoolExecutor(max_workers=3)
time.sleep(60)
executor.submit(bcjp_task.execute)
time.sleep(60)
executor.submit(bcen_task.execute)
time.sleep(60)
executor.submit(ac_task.execute)
