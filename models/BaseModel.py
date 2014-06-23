import peewee
from peewee import *

db = MySQLDatabase('feedbacks', host="localhost", user='root', passwd='admin')

class BaseModel(peewee.Model):
    class Meta:
        database = db