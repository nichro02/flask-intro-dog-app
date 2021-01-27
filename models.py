from peewee import *

import datetime

DATABASE = PostgresqlDatabase('dogs_app', host='localhost', port=5432)

class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog], safe=True)
    print('Tables created')
    DATABASE.close()