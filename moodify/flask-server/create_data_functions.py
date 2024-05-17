import requests
import json
from spotify_auth import get_access_token
import time

# Global variable to store the access token
access_token = None
all_tracks_data = {}
requests_per_second = 15

def get_playlist(playlist_id):
    global access_token
    
    SPOTIFY_GET_PLAYLIST_URL = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    
    # Ensure access token is available
    if not access_token:
        access_token = get_access_token()
    
    response = requests.get(
        SPOTIFY_GET_PLAYLIST_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    # Handle 401 Unauthorized error
    if response.status_code == 401:
        access_token = get_access_token()  # Get a new access token
        print("New Access Token:", access_token)
        response = requests.get(
            SPOTIFY_GET_PLAYLIST_URL,
            headers={
                'Authorization': f'Bearer {access_token}',
            },
        )
    
    try:
        resp_json = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        resp_json = {}
    except Exception as e:
        print(f"Error processing response: {e}")
        resp_json = {}

    return resp_json


def get_unique_track_ids(playlist_ids, mood):
    global all_tracks_data
    
    interval = 1 / requests_per_second
    
    for playlist_id in playlist_ids:
        playlist_info = get_playlist(playlist_id)
        time.sleep(1.0)
        for item in playlist_info['tracks']['items']:
            track_id = item['track']['id'] 
            track_title = item['track']['name']
            track_features = get_song_features(track_id)
            time.sleep(1.0)
            all_tracks_data[track_id] = {
                "title": track_title,
                "features": track_features,
                "mood": mood
            }
            # print("Track ID: ", track_id, "Values: ", all_tracks_data[track_id])
            time.sleep(interval)

def get_title(id):
    global access_token
    
    SPOTIFY_GET_TITLE_URL = f'https://api.spotify.com/v1/tracks/{id}'
    
    # Ensure access token is available
    if not access_token:
        access_token = get_access_token()
    
    response = requests.get(
        SPOTIFY_GET_TITLE_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    # Handle 401 Unauthorized error
    if response.status_code == 401:
        access_token = get_access_token()  # Get a new access token
        print("New Access Token:", access_token)
        response = requests.get(
            SPOTIFY_GET_TITLE_URL,
            headers={
                'Authorization': f'Bearer {access_token}',
            },
        )
    
    try:
        resp_json = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        resp_json = {}
    except Exception as e:
        print(f"Error processing response: {e}")
        resp_json = {}
    
    return resp_json.get('name', '')

def get_song_features(id):
    global access_token
    SPOTIFY_GET_FEATURES_URL = f'https://api.spotify.com/v1/audio-features/{id}'
    
    # Ensure access token is available
    if not access_token:
        access_token = get_access_token()
    
    response = requests.get(
        SPOTIFY_GET_FEATURES_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    # Handle 401 Unauthorized error
    if response.status_code == 401:
        access_token = get_access_token()  # Get a new access token
        print("New Access Token:", access_token)
        response = requests.get(
            SPOTIFY_GET_FEATURES_URL,
            headers={
                'Authorization': f'Bearer {access_token}',
            },
        )
    
    try:
        resp_json = response.json()
        features_list = [
            resp_json.get("danceability", 0),
            resp_json.get("energy", 0),
            resp_json.get("loudness", 0),
            resp_json.get("mode", 0),
            resp_json.get("acousticness", 0),
            resp_json.get("valence", 0),
            resp_json.get("tempo", 0)
        ]
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        features_list = [0] * 8
    except Exception as e:
        print(f"Error processing response: {e}")
        features_list = [0] * 8

    return features_list

def main():
    global access_token
    global all_tracks_data
    
    # Set up playlist IDs
    happy_playlist_ids = ['37i9dQZF1DX9XIFQuFvzM4', '37i9dQZF1DX889U0CL85jj', '37i9dQZF1DX8Dc28snyWrn', '37i9dQZF1DWYBO1MoTDhZI', '37i9dQZF1DX4fpCWaHOned', '37i9dQZF1DWSf2RDTDayIx', '37i9dQZF1DXa19sXUAHiO1', '37i9dQZF1DX7KNKjOK0o75', '37i9dQZF1DX2sUQwD7tbmL', '37i9dQZF1DWYzpSJHStHHx', '37i9dQZF1DX1BzILRveYHb', '37i9dQZF1DX6fhMYWIyuww']
    sad_playlist_ids = ['37i9dQZF1DWSqBruwoIXkA', '37i9dQZF1DWW2hj3ZtMbuO', '37i9dQZF1DX7gIoKXt0gmx', '37i9dQZF1DWZrBs4FjpxlE', '37i9dQZF1DX59NCqCqJtoH', '37i9dQZF1DWVV27DiNWxkR', '37i9dQZF1DWVrtsSlLKzro', '37i9dQZF1DWZUAeYvs88zc', '37i9dQZF1DWU4lunzhQdRx', '37i9dQZF1DWV1bxlagjEmb', '37i9dQZF1DX9AnYEthXLyU', '37i9dQZF1DX15JKV0q7shD']
    
    # Get unique track IDs
    get_unique_track_ids(happy_playlist_ids, "happy")
    # print("DONE HAPPY SET!")
    get_unique_track_ids(sad_playlist_ids, "sad")
    # print("DONE SAD SET!")
        
    return all_tracks_data

if __name__ == "__main__":
    main()