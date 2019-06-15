import pymongo
from pymodm import MongoModel, fields
from utils.utils import get_timestamp

from utils.config import conf


class AdminCode(MongoModel):
    code = fields.CharField(required=True, blank=False)

class User(MongoModel):
    username = fields.CharField(required=True, blank=False)
    password = fields.CharField(required=True, blank=False)
    email = fields.CharField(required=True, blank=False)
    type = fields.CharField(required=True, blank=False)
    code = fields.CharField(required=True,blank=False)



    

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

class VerificationCode(MongoModel):
    user_id = fields.ReferenceField(User, required=True)
    code = fields.CharField(required=True)
    create_at = fields.DateTimeField(required=True, default=get_timestamp)

    class Meta:
        indexes = [
            pymongo.IndexModel([('user_id', pymongo.ASCENDING)]),
            pymongo.IndexModel([('create_at', pymongo.ASCENDING)], expireAfterSeconds=conf['expire_time'])
        ]


