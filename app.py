from flask import Flask, request, render_template,  abort, redirect, url_for, session, escape
from .routes.index import Routeclass
from .config.db import db
import mongo_python_flask_skeleton.config.devConfig as config
import sys
sys.path.append("..")
app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = config.SECRET_KEY
app.debug = config.DEBUG
app.register_blueprint(Routeclass.routes)
app.config.from_pyfile('config/devConfig.py', silent=True)
app.config['MONGODB_SETTINGS'] = {
    'db': config.DB_NAME,
    'host': config.DB_HOST,
    'port': config.DB_PORT
}
