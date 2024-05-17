import requests
from pprint import pprint # Prints dictionaries nicely.
from spotify_auth import get_access_token
import json

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'

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
        "mood": None
    }
    try:
        resp_json = response.json()
        current_info['type'] = resp_json['currently_playing_type'] # Track, episode, ad, or none
        if current_info['type'] == 'track':
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
        elif current_info['type'] == 'episode':
            current_info['name'] = 'Podcast'
            current_info['image'] = 'https://blog.namarora.me/images/ayuj_browsing.jpeg'
            current_info['artists'] = ['Podcaster']
            current_info['mood'] = 'Starstruck'
        elif current_info['type'] == 'ad':
            current_info['name'] = 'Advertisement'
            current_info['image'] = 'https://blog.namarora.me/images/ayuj_browsing.jpeg'
            current_info['artists'] = ['Coporate America']
            current_info['mood'] = 'Impatient'
        else:
            current_info['name'] = 'Offline'
            current_info['image'] = 'https://blog.namarora.me/images/ayuj_sleeping.jpeg'
            current_info['artists'] = ['Ayuj']
            current_info['mood'] = 'Asleep'

    except json.JSONDecodeError as e:
        # Handle the case where JSON decoding fails (e.g., when Spotify is closed)
        print(f"Error decoding JSON response: {e}")

        # Set default values for current_info
        current_info['name'] = 'Offline'
        current_info['image'] = 'https://blog.namarora.me/images/ayuj_sleeping.jpeg'
        current_info['artists'] = ['Ayuj']
        current_info['mood'] = 'Asleep'
    except Exception as e:
        print(f"Error processing response: {e}")
    print(current_info)
    return current_info