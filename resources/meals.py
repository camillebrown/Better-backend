import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_user
from flask_login import login_user, logout_user, current_user, login_required

meals = Blueprint("meals", "meals")

@meals.route('/', methods=['GET'])
@login_required
def get_meals():
    try:
        meals = [model_to_dict(meal) for meal in models.Meal.select()\
                .join_from(models.Meal, models.Person)\
                .where(models.Person.id==current_user.id)]
        return jsonify(data=meals, status={"code": 200, "message": "Successfully pulled all meals"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the meals"})
    
@meals.route('/', methods=['POST'])
@login_required
def create_meal():
    payload = request.get_json()
    payload['person_id'] = current_user.id
    meal = models.Meal.create(**payload)
    meal_dict = model_to_dict(meal)
    return jsonify(data=meal_dict, status={"code": 201, "message":"Successfully created a new meal!"})

@meals.route('/<meal_id>', methods=["GET"])
@login_required
def get_meal(meal_id):
    try:
        meal = models.Meal.get_by_id(meal_id)
        meal_dict = model_to_dict(meal)
        return jsonify(data=meal_dict, status={"code": 200, "message": "Successfully grabbed single meal"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the meal"})
        
@meals.route('/<meal_id>', methods=["PUT"])
@login_required
def update_meal(meal_id):
    try:
        payload = request.get_json()
        query = models.Meal.update(**payload).where(models.Meal.id==meal_id)
        query.execute()
        updated_meal = model_to_dict(models.Meal.get_by_id(meal_id))
        return jsonify(data=updated_meal, status={"code": 200, "message": "Successfully updated the meal"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the meal"})

@meals.route('/<meal_id>', methods=["Delete"])
def delete_meal(meal_id):
    try:
        meal_to_delete = models.Meal.get_by_id(meal_id)
        meal_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Meal successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Meal does not exist"})
        