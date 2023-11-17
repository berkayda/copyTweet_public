import tweepy
import random
from datetime import datetime
import pytz
import time
istanbul_timezone = pytz.timezone("Europe/Istanbul")

consumer_key = "WRITEYOURS"
consumer_secret = "WRITEYOURS"
access_token = "WRITE-YOURS"
access_token_secret = "WRITEYOURS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Define special words
with open('special_words.txt', 'r') as file:
    special_words = [word.strip() for word in file.readlines()]

# Define user whose tweets will be fetched
username = "financialjuice"

while True:
    # Get the user's latest tweet
    try:
        tweets = api.user_timeline(screen_name=username, count=1)
        tweet = tweets[0]
        if not tweet.retweeted and 'RT @' not in tweet.text and not tweet.is_quote_status:
            # Make all text lowercase
            text = tweet.text.lower()

            # Replace special words with capitalized versions
            for word in special_words:
                capitalized_word = word.capitalize()
                text = text.replace(word, capitalized_word)

            # Check if the tweet has already been copied
            with open('copied_tweets.txt', 'r') as f:
                copied_tweets = f.read().splitlines()
            if tweet.id_str in copied_tweets:
                print("Latest tweet has already been copied.")
                print()
            else:
                # Tweet the modified text
                api.update_status(text + " #BREAKINGNEWS")

                # Write the tweet ID to the file of copied tweets
                with open('copied_tweets.txt', 'a') as f:
                    f.write(tweet.id_str + '\n')

                # Display current time and tweet text
                now = datetime.utcnow()
                now = now.replace(tzinfo=pytz.utc)  # Convert UTC time to Istanbul time
                time_of_calculation = now.astimezone(istanbul_timezone).strftime("%d-%m-%Y %H:%M:%S TSİ")
                print(f"Tweet copied at {time_of_calculation}:\n{text}")
                print()
        else:
            print("Latest tweet is a retweet or quote; text will not be copied.")
            print()
    except tweepy.TweepError as e:
        print("Error fetching latest tweet:", e)
        print()
    time.sleep(300)
