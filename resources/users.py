import models

from flask import Blueprint, jsonify, request, session, g, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required, confirm_login
from flask.sessions import SecureCookieSessionInterface
from playhouse.shortcuts import model_to_dict


users = Blueprint("users", "users")


@users.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
        # make the inputted email lowercase
    payload['email'].lower()
    
    try:
        models.Person.get(models.Person.email == payload['email'])
        return jsonify(data={},
                       status={"code": 401,
                               "message": "A user with that email already exists."})
    except models.DoesNotExist:
        # if the user does not already exist... create a user
        payload['password'] = generate_password_hash(payload['password'])
        user = models.Person.create(**payload)
        print('!!!!!!!!!!!!!!!!!!CREATED USER!!!!!!!!!!!!!!!!!!')
        user_dict = model_to_dict(user)
        del user_dict['password']  # Don't expose password!
        login_user(user=user, remember=True)
        print('!!!!!!!!!!!!!!!!!!USER LOGGED IN!!!!!!!!!!!!!!!!!!', user)
        session['logged_in'] = True
        print('???????????????SESSION SAVED???????????????', session['logged_in'])
        return jsonify(data=user_dict, status={"code": 201, "message": "Successfully registered user"})


@users.route('/login', methods=["POST"])
def login():
    # payload should contain email and password
    payload = request.get_json()
    # make the inputted email lowercase
    payload['email'].lower()
    try:
        # see if user is registered
        user = models.Person.get(models.Person.email == payload['email'])
        print('!!!!!!!!!!!!!!!!!!USER FOUND!!!!!!!!!!!!!!!!!!', user)
        user_dict = model_to_dict(user)
        print('!!!!!!!!!!!!!!!!!!USER DICT CREATED!!!!!!!!!!!!!!!!!!', user_dict)
        if(check_password_hash(user_dict['password'], payload['password'])):
            print('!!!!!!!!!!!!!!!!!PASSWORD CORRECT!!!!!!!!!!!!!!!!!!')
            del user_dict['password']
            session.pop('person_id', None)
            login_user(user=user, remember=True)
            session['logged_in'] = True
            session['person_id'] = user.id
            print('!!!!!!!!!!!!!!!!!!SESSION STARTED!!!!!!!!!!!!!!!!!!')
            login_user(user=user, remember=True)
            session['logged_in'] = True
            session['username'] = user.username
            g.user = user.username
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={'stats': 'username or password is incorrect'}, status={"code": 401, "message": "Username or password is incorrect."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or password is incorrect."})


@users.route('/', methods=["GET"])
def get_user():
    try:
        user = [model_to_dict(user) for user in
                  models.Person.select()
                  .where(models.Person.id == current_user.id)]
        return jsonify(data=user, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={},
                       status={"code": 401, "message": "Log in or sign up to view your profile."})

@users.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    try:
        logout_user()
        session.pop()
        session.clear()
        return jsonify(data={}, status={"code": 200, "message": "Successfully logged out"})
    except:
            return jsonify(data={}, status={"code": 401, "message": "No user logged in"})

