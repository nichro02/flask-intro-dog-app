import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

#setting up blueprint
# first argument is blueprints name
# second argument is its import_name
dog = Blueprint('dogs', 'dog')

@dog.route('/', methods=["GET"])
def get_all_dogs():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        #query DB to get all dogs
        all_dogs = models.Dog.select()
        #print(all_dogs)
        #parse the models into dictionaries
        dogs_to_dict = [model_to_dict(dog) for dog in all_dogs]
        #print(dogs_to_dict)
        return jsonify(data=dogs_to_dict, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Error getting the resources"})

@dog.route('/', methods=["POST"])
def create_dogs():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    #print(type(payload), 'payload')
    #create a dog -> ** is spread operator for dictionaries
    dog = models.Dog.create(**payload)
    ## see the object
    #print(dog.__dict__)
    ## Look at all the methods
    #print(dir(dog))
    # Change the model to a dict
    #print(model_to_dict(dog), 'model to dict')
    #parse dog so we can user jsonify
    dog_dict = model_to_dict(dog)
    return jsonify(data=dog_dict, status={"code": 201, "message": "Success"})

@dog.route('/<dog_id>', methods=["GET"])
def get_dog(dog_id):
    try:
        dog = models.Dog.get_by_id(dog_id)
        dog_dict = model_to_dict(dog)
        return jsonify(data=dog_dict, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={},status={"code": 404,\
                                       "message": "Error getting the resources"})

@dog.route('/<dog_id>', methods=["PUT"])
def update_dog(dog_id):
    try:
        payload = request.get_json()
        query = models.Dog.update(**payload).where(models.Dog.id==dog_id)
        query.execute()
        updated_dog = model_to_dict(models.Dog.get_by_id(dog_id))
        return jsonify(data=updated_dog, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={},status={"code": 404,\
                                       "message": "Error getting the resources"})

@dog.route('/<dog_id>', methods=["Delete"])
def delete_dog(dog_id):
    try:
        dog_to_delete = models.Dog.get_by_id(dog_id)
        dog_to_delete.delete_instance()
        return jsonify(data={}, status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={},status={"code": 404,\
                                       "message": "Error getting the resources"})