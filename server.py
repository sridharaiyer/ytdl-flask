#!/usr/bin/env python3
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import gevent.monkey
import sockets
import os

DOWNLOAD_DIR = os.path.expanduser('~/Downloads')

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', ping_timeout=30)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/downloads/<path:path>')
def send_downloaded(path):
    return send_from_directory(DOWNLOAD_DIR, path)


if __name__ == "__main__":
    gevent.monkey.patch_all()
    socketio.on('connect')(sockets.create_user)
    socketio.on('disconnect')(sockets.destroy_user)
    socketio.on('parse')(sockets.parse_url)
    socketio.on('start_dl')(sockets.start_dl)
    socketio.run(app, '0.0.0.0', 8001)
