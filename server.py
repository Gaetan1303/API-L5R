from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "API-L5R Socket.IO server is running."

@socketio.on('message')
def handle_message(data):
    print('Message reçu :', data)
    emit('message', {'response': f"Message reçu : {data}"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
