import models

from flask import Blueprint, jsonify, request
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

user_dogs = Blueprint('user_dogs', 'user_dogs')

@user_dogs.route('/', methods=['POST'])
def create_dogs():
    #create dog
    if current_user.id:
        payload = request.get_json()
        print(payload)
        dog = models.Dog.create(**payload)
        dog_dict = model_to_dict(dog)
    
        #breakpoint()

        #create relationship between dog and user
        #can be done through foreign key field on dog, or with a through table like below
        #YOU NEED TO BE LOGGED IN 
        user_dog_data = {
            'user': current_user.id,
            'dog': dog.id
        }
        models.UserDog.create(**user_dog_data)
        return jsonify(data=dog_dict, status={"code": 201, "message": "Success"})