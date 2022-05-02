'''Predicting text py file'''
import numpy as np
from .models import User
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''Determines which user is more likely to have tweeted
    the input string tweet. Fit our model to get predictions'''

    # Get the users from DB to compare
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # 2D numpy arrays - get tweet vects of user tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vects cobine into X matrix
    X = np.vstack([user0_vects, user1_vects])

    # 0 and 1 to generate Y vector
    y = np.concatenate([np.zeros(len(user0_vects)), np.ones(len(user1_vects))])

    # train logistic regression
    lr = LogisticRegression()
    lr.fit(X, y)

    # retrieve word embeddings for tweet
    tweet_emb = np.array([vectorize_tweet(hypo_tweet_text)])

    # generate predictions
    pred = lr.predict(tweet_emb)

    return pred[0]
