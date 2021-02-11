import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

meals = Blueprint("meals", "meals")

@meals.route('/', methods=['GET'])
def get_meals():
    try:
        meals = [model_to_dict(meal) for meal in models.Meal.select()]
        print(meals)
        return jsonify(data=meals, status={"code": 200, "message": "Successfully pulled all meals"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the meals"})
    
@meals.route('/', methods=['POST'])
def create_meal():
    payload = request.get_json()
    print(type(payload), 'payload')
    meal = models.Meal.create(**payload)
    print(meal.__dict__)
    print(dir(meal))
    print(model_to_dict(meal), 'model to dict')
    meal_dict = model_to_dict(meal)
    return jsonify(data=meal_dict, status={"code": 201, "message":"Successfully created a new meal!"})

@meals.route('/<meal_id>', methods=["GET"])
def get_meal(meal_id):
    try:
        meal = models.Meal.get_by_id(meal_id)
        meal_dict = model_to_dict(meal)
        return jsonify(data=meal_dict, status={"code": 200, "message": "Successfully grabbed single meal"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the meal"})
        
@meals.route('/<meal_id>', methods=["PUT"])
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
        