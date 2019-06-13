import pymongo
from pymodm import MongoModel, fields
from utils.utils import get_timestamp




class User(MongoModel):
    username = fields.CharField(required=True, blank=False)
    password = fields.CharField(required=True, blank=False)
    email = fields.CharField(required=True, blank=False)
    type = fields.CharField(required=True, blank=False, choices=['admin', 'visitor'])



    

    class Meta:
        indexes = [
            pymongo.IndexModel([('username', pymongo.ASCENDING)]),
            pymongo.IndexModel([('email', pymongo.ASCENDING)])
        ]

class Content(MongoModel):
    title = fields.CharField(required=True, blank=False)
    content = fields.CharField(required=True, blank=False)
    author = fields.ReferenceField(User, required=True)
    create_at = fields.DateTimeField(required=True, default=get_timestamp)


