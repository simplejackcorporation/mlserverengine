import threading
import json
import numpy as np
from time import sleep

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class ResponsesQueue(object):
    def __init__(self, image_queue, socketio):
        self.image_queue = image_queue
        self.socketio = socketio

        send_pred_thread = threading.Thread(target=self.startSendPredictions)
        print("\n\n\n\n")
        print("current thread ident", threading.currentThread().ident)

        send_pred_thread.daemon = True
        send_pred_thread.start()

    def startSendPredictions(self):
        while True:
            # print("while start send preds thread ident", threading.currentThread().ident)
            # print("preds len" , len(self.image_queue.predictions))

            if len(self.image_queue.predictions) > 0:
                print("VOVA")
                prediction = self.image_queue.predictions.pop(0)
                ys = prediction[:, :, 0][0]
                xs = prediction[:, :, 1][0]
                confs = prediction[:, :, 2][0]

                dumped_xs = json.dumps(ys, cls=NumpyEncoder)
                dumped_ys = json.dumps(xs, cls=NumpyEncoder)
                dumped_confs = json.dumps(confs, cls=NumpyEncoder)

                self.socketio.emit('model did predict', {"dumped_xs": dumped_xs,
                                                    "dumped_ys": dumped_ys,
                                                    "dumped_confs": dumped_confs})
                print("socket emited")
            sleep(1)


