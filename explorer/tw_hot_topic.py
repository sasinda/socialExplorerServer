import tweepy
import RAKE
import re
import json
from collections import Counter

def updateInPlace(a,b):
	a.update(b)
	return a

def json_for_twitter(access_token, access_token_secret): 
	# Consumer keys and access tokens, used for OAuth
	consumer_key = 'D7ZIV69VbyVZKXHyMKnVYB2q3'
	consumer_secret = 'AQimKid11GDXauW3BWKw0T8xAj415A5Uk5x6WPf5DFDyFpqV2l'
	 
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	user = api.me()

	me_id = user.name

	dic = {}
	for tweet in tweepy.Cursor(api.user_timeline,
							   id=me_id,
							   count=100,
							   result_type="recent",
							   include_entities=True,
							   lang="en").items():
		YM = str(tweet.created_at)[:7]
		
		
		if YM == "2015-08": break

		text = tweet.text.encode("GBK", 'ignore')

		text = text.replace("\n", " ")
		text = text.replace("//", "")
		text = text.replace("&amp", "")


		rake_object = RAKE.Rake("SmartStoplist.txt")

		
		keywords = rake_object.run(text)

		if not YM in dic:
			dic[YM] = keywords
			print YM
		else:
			dic[YM] = dic[YM] + keywords

	xValue = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
	yValue = []
	zValue = []
	text = []

	for YM in dic:
		YM_change = YM.replace("-","/")
		print YM_change
		yValue.append(YM_change)
		return_list = reduce(updateInPlace, [Counter({x[0]:x[1]}) for x in dic[YM]]).most_common(10)
		text_list = []
		number_list = []

		for item in return_list:
			text_list.append(item[0].decode("utf-8", "ignore"))
			number_list.append(item[1])
		zValue.append(number_list)
		text.append(text_list)


	return json.dumps({"x": xValue, "y": yValue, "z": zValue, "text": text, "type":"heatmap"})

print json_for_twitter('709076877797953536-H9vqKoaDXBBspoWcLRWGlTbu2utuvdw', 'pzsRqvFAmMz0EZ4TGXyq4dMarCcdXWABZvmqKax6jWFjs')
