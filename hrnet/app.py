from starlette.applications import Starlette
from starlette.responses import StreamingResponse
import uvicorn
import os
import websockets
import cv2
import base64

from starlette.templating import Jinja2Templates

app = Starlette()

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
templates = Jinja2Templates(directory='templates')

@app.route("/", methods = ["GET"])
async def homepage(request):
    return templates.TemplateResponse('home.html', {'request': request})

async def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            image_string = base64.b64encode(buffer)#.decode('utf-8')

            uri = "ws://localhost:8009"
            async with websockets.connect(uri) as websocket:
                name = image_string

                await websocket.send(name)
                greeting = await websocket.recv()
                print(f"< {greeting}")

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

def startApp():
    port = int(os.environ.get("PORT", 8008))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    startApp()
