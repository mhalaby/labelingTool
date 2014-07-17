import peewee
from peewee import *
import BaseModel as baseModel
        
class User(baseModel.BaseModel):
    id = CharField(primary_key=True)
    password = CharField()
    username = CharField()
