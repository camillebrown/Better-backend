from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.users import users
from resources.workouts import workouts
from resources.moods import moods
from resources.sleeps import sleeps
from resources.meals import meals
from resources.settings import settings

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.config.from_pyfile('config.py')

login_manager = LoginManager() # in JS: const loginManager = new LoginManager()
# take LoginManager instance (login_manager) and initialize it
# in an app (init_app()). The app we want it initialized in
# is called `app` (line 14)
login_manager.init_app(app) 

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.Person.get_by_id(user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE # MAKE SURE IT'S CAPS
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(app,\
    # add deployed link here too !!!!!
     origins=['http://localhost:3000'],\
     support_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(workouts, url_prefix='/workouts')
app.register_blueprint(moods, url_prefix='/moods')
app.register_blueprint(sleeps, url_prefix='/sleeps')
app.register_blueprint(meals, url_prefix='/meals')
app.register_blueprint(settings, url_prefix='/profile')

CORS(meals, 
     origins=['http://localhost:3000'],\
     support_credentials=True)

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
