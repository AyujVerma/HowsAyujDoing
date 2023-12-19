from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask import send_from_directory
from current_track import get_current_track, get_access_token

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/current-track')
def api_current_track():
    access_token = get_access_token()
    current_info = get_current_track(access_token)
    return jsonify(current_info)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected'})

@app.route('/')
def serve_react_app():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
