'''Predicting text py file'''
from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):

    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # 2D numpy arrays
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # X matrics for training lr
    vects = np.vstack([user0_vects, user1_vects])

    # 1D numpy arrays
    zeroes = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y vector(target) for training
    labels = np.concatenate([zeroes, ones])

    # Instantiate logreg
    log_reg = LogisticRegression()
    # train LR
    log_reg.fit(vects, labels)

    # vectorize - get word embeddings for
    # hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # get a prediction for which user said hypo tweet
    prediction = log_reg.predict(hypo_tweet_vect.reshape(1, -1))

    return prediction[0]
