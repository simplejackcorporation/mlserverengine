import os
import sys
import cv2
import torch

root_folder_path = os.path.split(os.getcwd())[0] # cd .. to root
sys.path.append(os.path.join(root_folder_path, 'hrnet'))
sys.path.append(root_folder_path)
os.chdir(root_folder_path)

from hrnet.SimpleHRNet import SimpleHRNet

import base64
import asyncio
import websockets
import numpy as np

model = SimpleHRNet(48, 17, device=torch.device("cuda"))

async def image_pred(websocket, path):
    # name = await websocket.recv()
    # image = base64.b64decode(name)
    # image = np.frombuffer(image, dtype=np.uint8)
    # image = cv2.imdecode(image, flags=1)
    # predictions = model.predict(image)
    # print(predictions)
    # print(predictions.shape)

    await websocket.send("{}".format("VOVA"))

if __name__ == "__main__":
    start_server = websockets.serve(image_pred, "localhost", 8009)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()