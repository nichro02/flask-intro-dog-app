from peewee import *
from flask_login import UserMixin

import datetime

DATABASE = PostgresqlDatabase('dogs_app', host='localhost', port=5432)

# set up base model
class BaseModel(Model):
    class Meta:
        database = DATABASE

#extending UserMixin allows us to use properties that helps us log user in
class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    #class Meta:
        #database = DATABASE

class Dog(BaseModel):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    #class Meta:
        #database = DATABASE

#through table
#backref allows us to grab dogs a user owns or the owner of a dog
#through dot notation 
class UserDog(BaseModel):
    user = ForeignKeyField(User, backref='pets')
    dog = ForeignKeyField(Dog, backref='human')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog, User, UserDog], safe=True)
    print('Tables created')
    DATABASE.close()