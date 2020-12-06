from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# app.config['PORT'] = 8009
app.config['DEBUG'] = True

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

@socketio.on('connect')
def test_connect():
    print("test_connect")
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    socketio.run(app, port=8009)
