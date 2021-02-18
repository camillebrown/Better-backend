import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user, current_user, login_required

workouts = Blueprint("workouts", "workouts")

@workouts.route('/', methods=['GET'])
@login_required
def get_workouts():
    # find the workouts and change each one to a dictionary in a new array
    try:
        print('THIS IS THE CURRENT USER', current_user)
        workouts = [model_to_dict(workout) for workout in models.Fitness.select()\
                    .join_from(models.Fitness, models.Person)\
                    .where(models.Person.id==current_user.id)]
        return jsonify(data=workouts, status={"code": 200, "message": "Successfully pulled all workouts"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the workouts"})
    
@workouts.route('/', methods=['POST'])
@login_required
def create_workout():
    payload = request.get_json()
    payload['person_id'] = current_user.id
    workout = models.Fitness.create(**payload)
    workout_dict = model_to_dict(workout)
    return jsonify(data=workout_dict, status={"code": 201, "message":"Successfully created a new workout!"})

@workouts.route('/<workout_id>', methods=["GET"])
@login_required
def get_workout(workout_id):
    try:
        print('THIS IS THE CURRENT USER', current_user)
        workout = models.Fitness.get_by_id(workout_id)
        workout_dict = model_to_dict(workout)
        return jsonify(data=workout_dict, status={"code": 200, "message": "Successfully grabbed single workout"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the workout"})
        
@workouts.route('/<workout_id>', methods=["PUT"])
@login_required
def update_workout(workout_id):
    try:
        payload = request.get_json()
        query = models.Fitness.update(**payload).where(models.Fitness.id==workout_id)
        query.execute()
        updated_workout = model_to_dict(models.Fitness.get_by_id(workout_id))
        return jsonify(data=updated_workout, status={"code": 200, "message": "Successfully updated the workout"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the workout"})

@workouts.route('/<workout_id>', methods=["Delete"])
@login_required
def delete_workout(workout_id):
    try:
        workout_to_delete = models.Fitness.get_by_id(workout_id)
        workout_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Workout successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Workout does not exist"})
        
