from pymongo import errors,MongoClient,ReturnDocument
import mongo_python_flask_skeleton.config.devConfig as config
try:
    client = MongoClient(config.DB_HOST, config.DB_PORT,serverSelectionTimeoutMS=100)
    client.server_info()
    db_name = config.DB_NAME
    db = client.blockcypher_practice
except errors.ServerSelectionTimeoutError as err:
    print(err)
    db = None