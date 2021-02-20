import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

# import logging

import models
from resources.users import users
from resources.workouts import workouts
from resources.moods import moods
from resources.sleeps import sleeps
from resources.meals import meals
from resources.settings import settings

DEBUG = True
PORT = 8000

# instantiate the app
app = Flask(__name__)

# create our session secret key
app.config.from_pyfile('config.py')

login_manager = LoginManager() # in JS -- const loginManager = new LoginManager()
login_manager.init_app(app) # initialize the new LoginManager instance in our app

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Person.get_by_id(user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'This Flask App works!'

CORS(app,\
     origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)
# CORS(moods,\
#      origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)
# CORS(settings,\
#      origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)
# CORS(workouts,\
#      origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)
# CORS(meals,\
#      origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)
# CORS(sleeps,\
#      origins=['http://localhost:3000', 'https://better-you-app.herokuapp.com'],\
#      supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(workouts, url_prefix='/workouts')
app.register_blueprint(moods, url_prefix='/moods')
app.register_blueprint(sleeps, url_prefix='/sleeps')
app.register_blueprint(meals, url_prefix='/meals')
app.register_blueprint(settings, url_prefix='/profile')

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(port=8000, debug=True)