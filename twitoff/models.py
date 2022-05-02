'''model class and tweet class to connect to DB'''
from flask_sqlalchemy import SQLAlchemy

# creating and connecting to DB
DB = SQLAlchemy()


class User(DB.Model):
    '''getting and inputer user data into DB'''
    # id
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"<User: {self.username}>"


class Tweet(DB.Model):
    '''getting tweets of user in DB
        getting vectors of those tweets
        loading them into DB for comparison'''

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
                        'user.id'), nullable=False)
    # user...attribute
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"<Tweet: {self.text}>"
