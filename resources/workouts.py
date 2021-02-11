import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name (.py file name)
# second argument is it's import_name (how will you import it into app.py)
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
workouts = Blueprint("workouts", "workouts")

@workouts.route('/', methods=['GET'])
def get_workouts():
    # find the workouts and change each one to a dictionary in a new array
    try:
        workouts = [model_to_dict(workout) for workout in models.Fitness.select()]
        print(workouts)
        return jsonify(data=workouts, status={"code": 200, "message": "Successfully pulled all workouts"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the workouts"})
    
@workouts.route('/', methods=['POST'])
def create_workout():
    payload = request.get_json()
    print(type(payload), 'payload')
    workout = models.Fitness.create(**payload)
    print(workout.__dict__)
    print(dir(workout))
    print(model_to_dict(workout), 'model to dict')
    workout_dict = model_to_dict(workout)
    return jsonify(data=workout_dict, status={"code": 201, "message":"Successfully created a new workout!"})

@workouts.route('/<workout_id>', methods=["GET"])
def get_workout(workout_id):
    try:
        workout = models.Fitness.get_by_id(workout_id)
        workout_dict = model_to_dict(workout)
        return jsonify(data=workout_dict, status={"code": 200, "message": "Successfully grabbed single workout"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the workout"})
        
@workouts.route('/<workout_id>', methods=["PUT"])
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
def delete_workout(workout_id):
    try:
        workout_to_delete = models.Fitness.get_by_id(workout_id)
        workout_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Workout successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Workout does not exist"})
        