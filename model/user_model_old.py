from ..config.db import db#,ReturnDocument
from flask import jsonify
from bson import json_util, ObjectId
import hashlib
import json
from ..schema.userSchema import User
from ..config.encoder import MyEncoder


class UserModel():
    def __init__(self):
        self.conn = db
        self.hash = hashlib
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    def get_user(self):
        #data = []
        # cursor = self.conn.users.find({ '$and':[{ 'email': 'jogi22@yopmail.com'}] }, {"_id": 0,'password':0,'address_private_key':0,'address_public_key':0})
        cursor = User.objects(email = 'ashish10@yopmail.com').first()
        data = json.loads(cursor.to_json())
        return jsonify({'status':1,"response": data})

    def update_faucet(self, data):
        updated_user = self.conn.users.find_one_and_update({'email':data.get('email')}, {"$set": {'faucet': 3}}) #return_document=ReturnDocument.AFTER
        data = json.loads(json_util.dumps(updated_user))
        return jsonify({'status':1,'data':data})

    def register(self, data):
        pwd = self.computeMD5hash(data.get('password'))
        email = data.get('email')
        email_data = self.conn.users.find_one({'email':email})
        if not email_data:
            tomodel = {'email':email,'password':pwd}
            result = self.conn.users.insert_one(tomodel)
            return result.inserted_id
        else:
            return None
    
    def computeMD5hash(self,my_string):
        result = self.hash.md5(my_string.encode())
        return result.hexdigest()
    
    def update_address(self,id_user,eth_address):
        print(id_user)
        updated_user = self.conn.users.find_one_and_update({'_id':id_user}, {"$set": {'eth_address': '0x'+eth_address['address'],'eth_private_key':eth_address['private']}})#,return_document=ReturnDocument.AFTER
        data = json.loads(json_util.dumps(updated_user))
        print(data)
        return data
    