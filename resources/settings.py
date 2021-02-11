import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

settings = Blueprint("settings", "settings")

# @settings.route('/', methods=['GET'])
# def get_settings():
#     try:
#         settings = [model_to_dict(setting) for setting in models.PersonSetting.select()]
#         print(settings)
#         return jsonify(data=settings, status={"code": 200, "message": "Successfully pulled all settings"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message":"Error getting the settings"})
    
@settings.route('/', methods=['POST'])
def create_new_setting():
    payload = request.get_json()
    print(type(payload), 'payload')
    setting = models.PersonSetting.create(**payload)
    print(setting.__dict__)
    print(dir(setting))
    print(model_to_dict(setting), 'model to dict')
    setting_dict = model_to_dict(setting)
    return jsonify(data=setting_dict, status={"code": 201, "message":"Successfully created settings for the user!"})

@settings.route('/account', methods=["GET"])
def get_meal():
    try:
        setting = models.PersonSetting.get_by_id(1)
        setting_dict = model_to_dict(setting)
        return jsonify(data=setting_dict, status={"code": 200, "message": "Successfully grabbed settings"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the settings"})
        
@settings.route('/account', methods=["PUT"])
def update_settings():
    try:
        payload = request.get_json()
        query = models.PersonSetting.update(**payload).where(models.PersonSetting.id==1)
        query.execute()
        updated_settings = model_to_dict(models.PersonSetting.get_by_id(1))
        return jsonify(data=updated_settings, status={"code": 200, "message": "Successfully updated the settings"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the settings"})

# @settings.route('/account', methods=["Delete"])
# def delete_all_settings():
#     try:
#         settings_to_delete = models.PersonSetting.get_by_id(1)
#         settings_to_delete.delete_instance()
#         return jsonify(data={}, status={"code": 200, "message": "All settings successfully deleted"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 404,\
#                                         "message": "All settings does not exist"})
        