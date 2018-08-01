from ..model.user_model import UserModel
from flask import jsonify,request
import mongo_python_flask_skeleton.config.devConfig as config
from web3 import Web3, HTTPProvider, IPCProvider
import pycurl
from io import StringIO
import blockcypher
import requests,json
from bson import json_util, ObjectId
user_model = UserModel()

class userController:
    def __init__(self):
        self.w3 = Web3(HTTPProvider('https://rinkeby.infura.io/'+config.WEB3_TOKEN))
        self.gasPriceGwei = 584
        self.gasLimit = 52968
        #Chain ID of Ropsten Test Net is 3, replace it to 1 for Main Net
        self.chainId = self.w3.net.chainId
        self.w3.eth.defaultAccount = config.ETH_MY_ADDR
        self.curl = pycurl.Curl()
    
    def getUsers(self):
        res = user_model.get_user()
        data = json.loads(json_util.dumps(res))
        return jsonify({'status':1, 'data':data})

    def updateFaucet(self,data):
        if not data.get('email'):
            return jsonify({'status':0,'msg':'required fields are missing!!'}), 400
        else:
            return user_model.update_faucet(data)

    def register(self):
        try:
            data = request.form
            if not (data.get('email') or data.get('password')):
                return jsonify({'status':0,'msg':'required fields are missing!!'}), 400
            else:
                id_user =  user_model.register(data)
                if id_user is None:
                    return jsonify({'status':0,'msg':'user already exists','data':[]}), 401
                else:
                    updated_data = self.update_address(id_user)
                    return jsonify({'status':1,'msg':'register successfully','data':updated_data}), 200
        except Exception:
            return jsonify({'status':0,'msg':'wooah, something really went wrong'}), 500

    def update_address(self,id_user):
        # data = request.form
        #eth_address = self.w3.personal.newAccount(data.get('password'))
        response = requests.post('https://api.blockcypher.com/v1/beth/test/addrs?token='+config.CYPHER_API_TOKEN)
        json_data = json.loads(response.text)
        return user_model.update_address(id_user,json_data)


    def generate_eth_address(self):
        print(config.CYPHER_API_TOKEN)
        # self.curl.setopt(self.curl.URL,'https://api.blockcypher.com/v1/beth/test/addrs?'+config.CYPHER_API_TOKEN)
        # response = self.curl.perform()
        # print(response)
        response = requests.post('https://api.blockcypher.com/v1/beth/test/addrs?token='+config.CYPHER_API_TOKEN)
        json_data = json.loads(response.text)
        return jsonify({'status':1,'address_data':json_data})

    def send_transaction(self):
        data = '{"inputs":[{"addresses": ["0xBA6EFC0fA4165F04B1A042C0a8dC7CC611c47423"]}],"outputs":[{"addresses": ["0x97240c3f465dafe983acf569e85642a4f435f413"], "value": 2100000000000000}]}'
        response = requests.post('https://api.blockcypher.com/v1/beth/test/txs/new?token='+config.CYPHER_API_TOKEN,data=data)
        json_data = json.loads(response.text)
        print(json_data)
        return jsonify({'status':1,'msg':'tx init','data':json_data})