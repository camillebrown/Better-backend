import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name (.py file name)
# second argument is it's import_name (how will you import it into app.py)
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
workouts = Blueprint("workouts", "workouts")