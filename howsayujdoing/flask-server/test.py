import requests
from spotify_auth import get_access_token

def get_track_audio_features(track_id, access_token):
    endpoint = f'https://api.spotify.com/v1/audio-features/{track_id}'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response containing audio features
    else:
        print(f"Failed to retrieve audio features. Status code: {response.status_code}")
        return None

# Example usage:
track_id = '11dFghVXANMlKmJXsNCbNl'
access_token = get_access_token()
audio_features = get_track_audio_features(track_id, access_token)

if audio_features:
    print("Audio Features:")
    print(audio_features)
