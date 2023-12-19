import os
import requests
from dotenv import load_dotenv # Loads .env file.
import json

# Load environment variables from the .env file
load_dotenv('auth.env')

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')
SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': SPOTIFY_REFRESH_TOKEN,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(auth_url, data=data)
    return response.json().get('access_token')

def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    # If the access token has expired, refresh it and retry the request.
    if response.status_code == 401:
        new_access_token = get_access_token()
        response = requests.get(
            SPOTIFY_GET_CURRENT_TRACK_URL,
            headers={
                'Authorization': f'Bearer {new_access_token}',
            },
        )
    current_info = {
        "type": None,
        "id": None,
        "name": None,
        "link": None,
        "duration": None,
        "progress": None,
        "image": None,
        "artists": None,
    }
    try:
        resp_json = response.json()
        current_info['type'] = resp_json['currently_playing_type'] # Track, episode, ad, or none
        if current_info['type'] == 'track' or current_info['type'] == 'episode':
            current_info['id'] = resp_json['item']['id']
            current_info['name'] = resp_json['item']['name']
            current_info['link'] = resp_json['item']['external_urls']['spotify']
            current_info['duration'] = resp_json['item']['duration_ms']
            current_info['progress'] = resp_json['progress_ms']
            current_info['image'] = resp_json['item']['album']['images'][0]['url']
            if current_info['type'] == 'track':
                artists = resp_json['item']['artists'] # Array of artist objects.
                artists_names = ', '.join(
                    [artist['name'] for artist in artists]
                )
                current_info['artists'] = artists_names
        elif current_info['type'] == 'ad':
            current_info['name'] = 'Advertisement'
            current_info['image'] = 'https://drive.google.com/uc?id=1dDSsjkDUX_2OM3iFTXxC1POubWCZObzH'
            current_info['artists'] = ['Coporate America']
        else:
            current_info['name'] = 'Offline'
            current_info['image'] = 'https://drive.google.com/uc?id=1U-vVukBvPqdjw23i1GTMSC_zXLR08soX'
            current_info['artists'] = ['Ayuj']

    except json.JSONDecodeError as e:
        # Handle the case where JSON decoding fails (e.g., when Spotify is closed)
        print(f"Error decoding JSON response: {e}")

        # Set default values for current_info
        current_info['name'] = 'Offline'
        current_info['image'] = 'https://drive.google.com/uc?id=1U-vVukBvPqdjw23i1GTMSC_zXLR08soX'
        current_info['artists'] = ['Ayuj']

    except Exception as e:
        print(f"Error processing response: {e}")
    return current_info