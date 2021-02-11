import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
import json

sleeps = Blueprint("sleeps", "sleeps")

@sleeps.route('/', methods=['GET'])
def get_sleep_logs():
    try:
        sleep_logs = [model_to_dict(sleep) for sleep in models.Sleep.select()]
        return json.dumps(sleep_logs, indent=4, sort_keys=True, default=str)
        # return jsonify(data=sleep_logs, status={"code": 200, "message": "Successfully pulled all sleep logs"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the sleep logs"})
    
@sleeps.route('/', methods=['POST'])
def create_sleep_log():
    payload = request.get_json()
    sleep = models.Sleep.create(**payload)
    sleep_dict = model_to_dict(sleep)
    return jsonify(data=sleep_dict, status={"code": 201, "message":"Successfully created a new sleep log!"})

@sleeps.route('/<sleep_id>', methods=["GET"])
def get_sleep_log(sleep_id):
    try:
        sleep = models.Sleep.get_by_id(sleep_id)
        sleep_dict = model_to_dict(sleep)
        return json.dumps(sleep_dict, indent=4, sort_keys=True, default=str)
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the sleep"})
        
@sleeps.route('/<sleep_id>', methods=["PUT"])
def update_sleep_log(sleep_id):
    try:
        payload = request.get_json()
        query = models.Sleep.update(**payload).where(models.Sleep.id==sleep_id)
        query.execute()
        updated_sleep = model_to_dict(models.Sleep.get_by_id(sleep_id))
        return json.dumps(updated_sleep, indent=4, sort_keys=True, default=str)
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the sleep log"})

@sleeps.route('/<sleep_id>', methods=["Delete"])
def delete_sleep_log(sleep_id):
    try:
        sleep_to_delete = models.Sleep.get_by_id(sleep_id)
        sleep_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Sleep log successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Sleep log does not exist"})
        