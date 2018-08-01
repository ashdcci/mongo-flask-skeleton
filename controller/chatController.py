from ..model.user_model import UserModel
from flask import jsonify,request
import mongo_python_flask_skeleton.config.devConfig as config
from web3 import Web3, HTTPProvider, IPCProvider
from web3.shh import Shh
import pycurl
from io import StringIO
import blockcypher
import requests,json
from bson import json_util, ObjectId
import threading
user_model = UserModel()


class chatController:
    def __init__(self):
        self.w3 = Web3(HTTPProvider('http://localhost:8545'))
        Shh.attach(self.w3, "shh")
        self.shh = self.w3.shh
        #Chain ID of Ropsten Test Net is 3, replace it to 1 for Main Net
        self.chainId = self.w3.net.chainId
        self.defaultTopic = "0x5a4ea131"
        self.privateKey = '0x862e3b865d47553509e7e97229a6e868c6656dd654799dd411ffbdcf8f2fa800'
        self.defaultRecipientPubKey = ''
        # self.data1 = L(
		# 	'msgs': '',
		# 	'text': "",
		# 	'symKeyId': '',
		# 	'name': "",
		# 	'asymKeyId': '',
		# 	'sympw': "",
		# 	'asym': True,
		# 	'configured': False,
		# 	'topic': self.defaultTopic,
		# 	'recipientPubKey': self.defaultRecipientPubKey,
		# 	'asymPubKey': ""
        # )
        # self.data ={}


        self.data = {
            'msgs': '',
			'text': "",
			'symKeyId': '',
			'name': "",
			'asymKeyId': '',
			'sympw': "",
			'asym': True,
			'configured': False,
			'topic': self.defaultTopic,
			'recipientPubKey': self.defaultRecipientPubKey,
			'asymPubKey': ""
        }
        # a = MyDict()
        # a.test = 'hello'
        # print('a',a)
        print('data: ',self.data)
        self.data['asymKeyId'] = '9acd5567090cfd678e2374b84374715d250bf3f867e8ac21952eba279e10b97c'
        self.data['asymPubKey'] = '0x0481cb49387b170626a4edc7642b213473a86cadf0ec781582013b6198c86ebe8c01c52f2a0c22b33ab17f1facaa1f58c7cd889b1d60e3963a2fb40459bf43beae'
        # setattr((self.data, 'asymKeyId', '9acd5567090cfd678e2374b84374715d250bf3f867e8ac21952eba279e10b97c')
        # setattr(self.data, 'asymPubKey', '0x0481cb49387b170626a4edc7642b213473a86cadf0ec781582013b6198c86ebe8c01c52f2a0c22b33ab17f1facaa1f58c7cd889b1d60e3963a2fb40459bf43beae')
        
        self.getFilterMessage()
        # threading.Timer(1.0, self.getFilterMessage).start()
        # while True:
        #     t.cancel()
        #     t.start()
        # self.defaultRecipientPubKey = self.shh.getPublicKey(self.data['asymKeyId'])
        
        
    @setInterval(1, 3)
    def getFilterMessage(self):
        filterCriteria = {'topic':self.defaultTopic,'privateKeyID': self.data['asymKeyId']} 
        print(filterCriteria)


        return

    def sendShhMessage(self):
        
        # res = self.shh.post({'payload': self.w3.toHex(text="test_payload"), 'pubKey': self.defaultRecipientPubKey, 'topic': '0x12340000', 'powTarget': 2.5, 'powTime': 2})        
        return jsonify({'status':1,'msg':'message sent','data':0})


class MyDict(object):
    pass




def setInterval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap