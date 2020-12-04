from starlette.applications import Starlette
import cv2
from SimpleHRNet import SimpleHRNet
import base64
import asyncio
import websockets
import numpy as np

app = Starlette()
model = SimpleHRNet(48, 17, "weights/pose_hrnet_w48_384x288.pth")

async def image_pred(websocket, path):
    name = await websocket.recv()
    image = base64.b64decode(name)
    image = np.frombuffer(image, dtype=np.uint8)
    image = cv2.imdecode(image, flags=1)
    predictions = model.predict(image)
    await websocket.send("{}".format(predictions))


if __name__ == "__main__":
    start_server = websockets.serve(image_pred, "localhost", 8009)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
