from flask import Flask, jsonify
from flask_cors import CORS
from flask import send_from_directory
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
    app.run(debug=True)