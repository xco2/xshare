# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, jsonify, make_response, render_template
from loguru import logger
import os, time
import base64
from flask_socketio import SocketIO, emit


def to_utf8(res):
    response = make_response(res)
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return response


app = Flask(__name__)

socketio = SocketIO()
socketio.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('test_socketio.html', async_mode=socketio.async_mode)


@app.route("/emitSockit", methods=["POST", "GET"])
def emit_sockit():
    data = {"a": "aaa", "b": "bbb", "c": "ccc", "d": "ddd"}
    emit('Change',
         data,
         broadcast=True, namespace="/testsocket")
    return jsonify({"code": 200})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)
