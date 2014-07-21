import peewee
from peewee import *
from flask import Flask,request

db = MySQLDatabase('feedbacks', host="localhost", user='root', passwd='admin', threadlocals=True)

class BaseModel(peewee.Model):
        
    class Meta:
        database = db
        
    def _connect(self):
        print "connecting"
        db.connect()  