from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from current_track import get_current_track, get_access_token
from create_data_functions import get_song_features
import numpy as np
import pickle

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
CORS(app)

@app.route('/api/current-track')
def api_current_track():
    access_token = get_access_token()
    current_info = get_current_track(access_token)
    if current_info['type'] == 'track':
        id = current_info['id']
        data = get_song_features(id)
        data_2D_arr = np.array(data).reshape(1, -1)
        prediction = loaded_model.predict(data_2D_arr)
        prediction_list = prediction.tolist()
        current_info['mood'] = prediction_list[0]
    return jsonify(current_info)

@app.route('/')
def serve_react_app():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    # Use Waitress as the production server
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
