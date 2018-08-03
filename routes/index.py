#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import environ
import sys
sys.path.append("..")
from flask import Flask, request, render_template,  abort, redirect, url_for, session, escape, Blueprint, jsonify

# print(global.socketio)
# socketio = getattr(g,'socketio',None)
### Controller Class Calling
from ..controller.userController import userController
from ..controller.chatController import chatController
userController = userController()
chatController = chatController()

class Routeclass(object):
    routes = Blueprint('api', __name__)
    @routes.route('/')
    def api():
        return render_template('index.html')

    @routes.route('/get-users')
    def get_users1():
        return userController.getUsers()

    @routes.route('/update-faucet',methods=['POST'])
    def updateFaucet():
        data = request.form
        return userController.updateFaucet(data)

    @routes.route('/register',methods=['POST'])
    def register():
        return userController.register()

    @routes.route('/new-eth-address')
    def generate_eth_address():
        return userController.generate_eth_address()

    @routes.route('/send-transaction',methods=['POST'])
    def send_transaction():
        return userController.send_transaction()

    @routes.route('/send-message',methods=['POST'])
    def send_message():
        return chatController.sendShhMessage()
  