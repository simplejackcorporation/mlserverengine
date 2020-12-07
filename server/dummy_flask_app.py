from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import threading
from engineio.payload import Payload
Payload.max_decode_packets = 50


import numpy as np

import os
import sys
import json

# root_folder_path = os.path.split(os.getcwd())[0] # cd .. to root
print("root folder path", os.getcwd())

sys.path.append(os.path.join(os.getcwd(), 'hrnet'))
sys.path.append(os.path.join(os.getcwd(), 'server'))

sys.path.append(os.getcwd())
# print(os.getcwd())
from hrnet.SimpleHRNet import SimpleHRNet
from server.image_prediction_queue import ImagePredictionQueue

import torch

app = Flask(__name__)
# app.config['PORT'] = 8009
app.config['DEBUG'] = True

cors = CORS(app)

# https://github.com/miguelgrinberg/python-engineio/issues/142
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent',  ping_timeout=1000, ping_interval=1000)

model = SimpleHRNet(48, 17, device=torch.device("cuda"))


# def queuecallback(prediction):
#     dumped = json.dumps(prediction, cls=NumpyEncoder)
#     socketio.emit('model did predict', {"prediction" : dumped})



image_queue = ImagePredictionQueue(socketio)

@app.route('/')
def index():
    print("index dummy flask")
    return render_template('home.html')

@socketio.on('connect')
def test_connect():
    print("test_connect")
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('send video')
def send_video(socket):
    print("send video")
    image_queue.appendImage(socket)

    emit('video received')


    # @copy_current_request_context
    # def temp():
    #     image_queue.appendImage(socket)
    # temp()
    # print(img_string)

    # emit("Video received")

if __name__ == '__main__':
    print("vova")
    socketio.run(app, port=8009)
