import peewee
from peewee import *
from playhouse.pool import *
from flask import Flask,request

db = PooledMySQLDatabase('feedbacks',    stale_timeout=None,
 host="localhost", user='root', passwd='admin', threadlocals=True)

class BaseModel(peewee.Model):
        
    class Meta:
        database = db
        
    def _connect(self):
        print "connecting"
        db.connect()  
    def _disconnect(self):
        print "disconnecting"
        db.close()  