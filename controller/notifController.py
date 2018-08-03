from flask import jsonify,request,render_template
from ..app import socketio

class notifController:
    def __init__(self):
        self.hello = ''

    @socketio.on('my_event')
    def handle_my_custom_event(json):
        print('received json: ' + str(json))  

