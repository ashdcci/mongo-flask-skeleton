from flask_mongoengine import MongoEngine
# from ..config.db import db
db = MongoEngine()
print(db)
import datetime

class User(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.EmailField()
    password = db.StringField(max_length = 255)
    access_token = db.StringField()
    user_address = db.StringField()
    address_private_key = db.StringField()
    address_public_key = db.StringField()
    address_wif = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
    deleted_at = db.StringField()
    __v = db.StringField()
    is_deleted = db.IntField(default=0)
    eth_address = db.StringField()
    eth_private_key = db.StringField()
    eth_pricate_key = db.StringField()
    faucet = db.IntField()
    meta = {
        'collection': 'users',
        'strict': False
    }