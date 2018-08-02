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
        self.defaultPwd = 'core2duo'
        self.kid = ''
        self.defaultkId = '8158692724d0353cdf336f843ebea2de6932d811e2e6b06cb5c18bec67d37866'
        self.payloadMsg = ''
        
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
        self.data['symKeyId'] = self.shh.generateSymKeyFromPassword(self.defaultPwd)
        print('data: ',self.data)
        self.getFilterMessage()
        
        
        
    def getFilterMessage(self):
         #self.shh.newKeyPair()
        res = self.shh.hasKeyPair(self.defaultkId)
        if not (res):
            self.kId=self.shh.addPrivateKey(self.privateKey)
            print('self new kid: ',self.kId)

        self.privateKey = self.shh.getPrivateKey(self.kId)
        self.defaultRecipientPubKey = self.shh.getPublicKey(self.kId)
        self.data['asymKeyId'] = self.privateKey

        print(res)
        print('kid: ',self.kId)
        print('gprk: ',self.privateKey)
        print('gpubk: ',self.defaultRecipientPubKey)
        filterCriteria = {'topic':self.defaultTopic,'symKeyId': self.data['symKeyId']} 
        print(filterCriteria)
        self.payloadMsg = self.shh.newMessageFilter(filterCriteria)
        # print('msgs: ',payloadMsg)
        # resMessage = self.shh.getMessages(payloadMsg.filter_id)
        # print(resMessage)
        return

    def sendShhMessage(self):
        data = request.form
        message = data.get('message')
        res = self.shh.post({
                'payload': self.w3.toHex(text=message),
                'symKeyId': self.data['symKeyId'], 
                'topic': self.defaultTopic,
                'powTarget': 2.5,
                'powTime': 2
                })
        print('message sent:',res)
        # self.getFilterMessage()
        resMessage = self.shh.getMessages(self.payloadMsg.filter_id)
        mes_pars = ''
        if resMessage != []:
            message = resMessage[0]
            mes_pars = message['payload']
            # mes_from = message['recipientPublicKey']
            topic = message['topic']
            # timestamp = message['timestamp']
            # print('from user => {}'.format(Web3.toHex(mes_from)))
            print('message => {}'.format(Web3.toText(mes_pars)))
            # print('topic => {}'.format(Web3.toText(topic)))
            # print('timestamp => {}'.format(timestamp))        

        print(resMessage)
        # print('message: ',self.w3.toText(resMessage['payload']))
        return jsonify({'status':1,'msg':'message sent','message':Web3.toText(mes_pars)})


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