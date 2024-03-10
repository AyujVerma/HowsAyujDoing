from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from current_track import get_current_track, get_access_token

app = Flask(__name__)
CORS(app)

@app.route('/api/current-track')
def api_current_track():
    access_token = get_access_token()
    current_info = get_current_track(access_token)
    return jsonify(current_info)

@app.route('/')
def serve_react_app():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    # Use Waitress as the production server
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
