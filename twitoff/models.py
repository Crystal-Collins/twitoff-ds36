'''a docstring'''
from flask_sqlalchemy import SQLAlchemy

# creating and connecting to DB
DB = SQLAlchemy()


class User(DB.Model):
    # id
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    # def __repr__(self):
    #     return f"<User: {self.name}>"


class Tweet(DB.Model):
    # id
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text
    text = DB.Column(DB.Unicode(300))
    # vect
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    # user...attribute
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"<Tweet: {self.text}>"
