
import os
from twitter.twitter_wrapper import TwitterApi
from discord.discord_wrapper import DiscordApi

class BCTask:
	account_jp_id = os.environ.get('BCJP_ACCOUNT_ID')
	account_en_id = os.environ.get('BCEN_ACCOUNT_ID')
	web_hook = os.environ.get('BATTLECAT_WEBHOOK')

	def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
		self.twitter = TwitterApi(consumer_key, consumer_secret, access_token, access_secret)
		self.discord = DiscordApi(self.web_hook)
		self.handle = {
			self.account_jp_id: self.handle_tweet_jp,
			self.account_en_id: self.handle_tweet_en
		}

	def handle_tweet_jp(self, tweet):
		text = self.translator.translate(tweet.text, dest='en').text
		if(text is None):
			text = tweet.text
		message = '\n========================================\n【BCJP】- Battle Cat JP Twitter\n========================================\n\n'+text
		self.discord.send_discord_message(message)

	def handle_tweet_en(self, tweet):
		message = '\n========================================\n【BCEN】- Battle Cat EN Twitter\n========================================\n\n'+tweet.text
		self.discord.send_discord_message(message)

	def handle_tweet(self, tweet):
		self.handle[tweet.userId](tweet)

	def execute(self):
		print("Starting up BCTask....")
		account_ids = [self.account_en_id, self.account_jp_id]
		self.twitter.on_status_change(self.account_id, self.handle_tweet)
