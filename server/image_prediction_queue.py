import threading
from time import sleep
import os
import sys
import torch
import cv2
import base64
import numpy as np
import json

# root_folder_path = os.path.split(os.getcwd())[0] # cd .. to root
print("root folder path", os.getcwd())

sys.path.append(os.path.join(os.getcwd(), 'hrnet'))
sys.path.append(os.path.join(os.getcwd(), 'facedetection'))

sys.path.append(os.getcwd())
# print(os.getcwd())
from hrnet.SimpleHRNet import SimpleHRNet




class ImagePredictionQueue(object):
    def __init__(self, socketio):
        self.model = SimpleHRNet(48, 17, device=torch.device("cuda"))

        self.socketio = socketio
        self.image_queue = []
        self.is_thread_started = False
        self.startThread()
        self.predictions = []


    def startThread(self):
        if self.is_thread_started is True:
            return
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()
        self.is_thread_started = True

    def appendImage(self, socket):
        if len(self.image_queue) == 0:
            print('appendImage')

            self.image_queue.append(socket)
        # sleep(0.01)

    def processImage(self):
        if len(self.image_queue) == 0:
            return

        print(len(self.image_queue))

        print("img process")
        socket = self.image_queue.pop(0)
        img_string = socket["data"].split(',')[1]
        image = base64.b64decode(img_string)
        image = np.frombuffer(image, dtype=np.uint8)
        image = cv2.imdecode(image, flags=1)

        prediction = self.model.predict(image)

        self.predictions.append(prediction)
        # ys = prediction[:, :, 0][0]
        # xs = prediction[:, :, 1][0]
        # confs = prediction[:, :, 2][0]
        #
        # dumped_xs = json.dumps(ys, cls=NumpyEncoder)
        # dumped_ys = json.dumps(xs, cls=NumpyEncoder)
        # dumped_confs = json.dumps(confs, cls=NumpyEncoder)
        #
        # self.socketio.emit('model did predict', {"dumped_xs" : dumped_xs,
        #                                          "dumped_ys" : dumped_ys,
        #                                          "dumped_confs" : dumped_confs})


        sleep(0.01)

    def start(self):
        while True:
            self.processImage()
            sleep(0.01)