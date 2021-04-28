from flask import Flask, request, jsonify, g, session, make_response
from flask_session import Session
from flask_cors import CORS
from flask_login import LoginManager
from flask.sessions import SecureCookieSessionInterface

from playhouse.db_url import connect
import os 

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
app.config['SECRET_KEY']=(os.environ.get('SECRET_KEY'))
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
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    g.db = models.DATABASE
    g.db.connect()
    
@app.after_request
def after_request(response):
    # same_cookie = session_cookie.dumps(dict(session))
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    response.headers.add("Set-Cookie", "my_cookie='a cookie'; Secure; SameSite=None;")
    g.db = models.DATABASE
    g.db.close()
    return response

@app.route('/')
def hello_world():
    resp = make_response('Hello, World!')
    return 'hello this flask app is working'

CORS(app,\
     origins=['http://localhost:3000', 'https://parks-passsport.vercel.app', 'https://parkspassport-api-heroku.herokuapp.com/'],\
     supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(workouts, url_prefix='/workouts')
app.register_blueprint(moods, url_prefix='/moods')
app.register_blueprint(sleeps, url_prefix='/sleeps')
app.register_blueprint(meals, url_prefix='/meals')
app.register_blueprint(settings, url_prefix='/profile')
CORS(users)
CORS(workouts)
CORS(moods)
CORS(sleeps)
CORS(meals)
CORS(settings)

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
    
if __name__ == '__main__':
    models.initialize()
    app.run(port=8000, debug=True)