from starlette.applications import Starlette
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

import uvicorn
import os
import websockets
import cv2
import base64
import numpy as np

import sys
root_folder_path = os.path.split(os.getcwd())[0] # cd .. to root
sys.path.append(os.path.join(root_folder_path, 'hrnet'))
sys.path.append(root_folder_path)
os.chdir(root_folder_path)


from hrnet.misc.visualization import draw_points_and_skeleton, joints_dict


temp_image = None

app = Starlette()
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), 'server', 'templates'))

async def vis_points(websocket):
    predictions = await websocket.recv()
    print(predictions)
    print(predictions[3:-3])

    # predictions = np.fromstring(predictions[1:-1], dtype=np.float_, sep=' ')

    # print(predictions.shape)

    # person_ids = np.arange(len(predictions), dtype=np.int32)
    # image = None
    # print(temp_image.shape)
    # for i, (pt, pid) in enumerate(zip(predictions, person_ids)):
    #     image = draw_points_and_skeleton(temp_image,
    #                                      pt,
    #                                      joints_dict()['coco']['skeleton'],
    #                                      person_index=pid,
    #                                      points_color_palette='gist_rainbow',
    #                                      skeleton_color_palette='jet',
    #                                      points_palette_samples=10)

    # cv2.imshow("temp", image)
    # cv2.waitKey(0)

async def gen_frames():  # generate frame by frame from camera
    global temp_image

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        temp_image = frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            image_string = base64.b64encode(buffer)#.decode('utf-8')

            uri = "ws://localhost:8009"
            async with websockets.connect(uri) as websocket:
                name = image_string

                await websocket.send(name)
                await vis_points(websocket)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/stream", methods = ["POST"])
def stream(request):
    return templates.TemplateResponse('camera_stream.html', {'request': request})


@app.route("/video_feed", methods=["GET"])
async def video_feed(scope):
    assert scope['type'] == 'http'
    generator = gen_frames()
    response = StreamingResponse(generator, media_type='multipart/x-mixed-replace; boundary=frame')
    return response


@app.route("/", methods = ["GET"])
async def homepage(request):
    return templates.TemplateResponse('home.html', {'request': request})

def startApp():
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    startApp()
