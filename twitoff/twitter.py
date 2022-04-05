'''twitter docstring'''

import tweepy
from os import getenv
from .models import DB
from .models import Tweet
from .models import User
import spacy


# our API keys
key = getenv("TWITTER_API_KEY")
secret = getenv("TWITTER_API_KEY_SECRET")

# Authenticate twitter
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)

# Open connection to API
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    # get user data from twitter
    try:
        twitter_user = TWITTER.get_user(screen_name=username)

        # check to see if user is in database
        # if in database, do nothing
        # or else, insert them
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, username=username))

        DB.session.add(db_user)

        # get users tweets
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add individual tweets to DB
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector,
                             user_id=db_user.id)

            DB.session.add(db_tweet)

    except Exception as error:
        print(f'Error when processing {username}: {error}')
        raise error
    else:
        DB.session.commit()


# Turn tweet text into word vector
alp = spacy.load('my_model/')


def vectorize_tweet(tweet_text):
    return alp(tweet_text).vector
