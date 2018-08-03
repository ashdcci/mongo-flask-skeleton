from flask import Flask, request, render_template,  abort, redirect, url_for, session, escape
from flask_socketio import SocketIO
from .routes.index import Routeclass

from .config.db import db
import mongo_python_flask_skeleton.config.devConfig as config
import sys
socketio = SocketIO()
sys.path.append("..")

def create_app(debug=False):
    app = Flask(__name__)
    socketio = SocketIO(app)
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
    socketio.init_app(app)
    return app