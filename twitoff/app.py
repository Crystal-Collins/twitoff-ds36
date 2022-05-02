'''flask app py file'''
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user

# Factory


def create_app():
    '''Twitoff  factory: all pages we route to'''

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def home():
        '''the home route creates home page'''
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route("/reset")
    def reset():
        '''resets the DB when users click the button'''
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    @app.route("/update")
    def update():
        '''updates the users list'''
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='Update Users')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        '''creates a route for adding users to DB for comparison'''
        name = name or request.value['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User "{name}" was successfully added.'

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f'Error adding "{name}"": {e}'
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        '''final comparison with results'''
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare users to themselves!'
        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'],
                user1 if prediction else user0,
                user0 if prediction else user1)

        return render_template('prediction.html', title='Prediction', message=message)

    return app
