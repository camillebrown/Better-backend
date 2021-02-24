import models
from flask import Blueprint, jsonify, request, session
from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager,login_required, current_user

moods = Blueprint("moods", "moods")

@moods.route('/', methods=['GET'])
@login_required
def get_moods():
    try:
        moods = [model_to_dict(mood) for mood in models.Mood.select()\
                .join_from(models.Mood, models.Person)\
                .where(models.Person.id==current_user.id)]
        ratings = [mood.get_rating() for mood in models.Mood.select()\
                  .join_from(models.Mood, models.Person)\
                  .where(models.Person.id==current_user.id)]
        return jsonify(data=moods, ratings=ratings, status={"code": 200, "message": "Successfully pulled all moods"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the moods"})
    
@moods.route('/', methods=['POST'])
@login_required
def create_mood():
    payload = request.get_json()
    payload['person_id'] = current_user.id
    mood = models.Mood.create(**payload)
    mood_dict = model_to_dict(mood)
    return jsonify(data=mood_dict, status={"code": 201, "message":"Successfully created a new mood log!"})

@moods.route('/<mood_id>', methods=["GET"])
@login_required
def get_mood(mood_id):
    try:
        mood = models.Mood.get_by_id(mood_id)
        rating = models.Mood.get_by_id(mood_id).get_rating()
        mood_dict = model_to_dict(mood)
        mood_dict['rating'] = rating
        return jsonify(data=mood_dict, status={"code": 200, "message": "Successfully grabbed single mood"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the mood"})
        
@moods.route('/<mood_id>', methods=["PUT"])
@login_required
def update_mood(mood_id):
    try:
        payload = request.get_json()
        query = models.Mood.update(**payload)\
                .where(models.Mood.id==mood_id)
        query.execute()
        updated_mood = model_to_dict(models.Mood.get_by_id(mood_id))
        return jsonify(data=updated_mood, status={"code": 200, "message": "Successfully updated the mood"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the mood"})

@moods.route('/<mood_id>', methods=["Delete"])
@login_required
def delete_mood(mood_id):
    try:
        mood_to_delete = models.Mood.get_by_id(mood_id)
        mood_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Mood successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Mood does not exist"})
        