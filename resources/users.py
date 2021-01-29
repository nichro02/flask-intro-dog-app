import models

from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'].lower()

    #Does user already exist/is username taken?
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={'code': 401,'message': 'user with email already exists'})
    except models.DoesNotExist:
        #if user does not exist, create user
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)

        print('BEFORE ------>', user_dict)
        #delete password key from user_dict
        del user_dict['password']
        print('AFTER --------->', user_dict)

        return jsonify(data=user_dict, status={'code': 201, 'message': 'user created'})

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'].lower()

    try:
        #check if user is registered
        user = models.User.get(models.User.email == payload['email'])
        print('USER!!!!!', user)

        user_dict = model_to_dict(user)

        #check password hash
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            #start session if password is correct
            login_user(user)
            return jsonify(data=user_dict, status={'code': 200, 'message': 'successful login'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'username or password is incorrect'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'username or password is incorrect'})

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify(data={}, status={'code': 200, 'message': 'logout successful'})
    
