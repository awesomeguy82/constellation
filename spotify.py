from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# https://www.youtube.com/watch?v=WAmEZBEeNmg&t=750s
# https://developer.spotify.com/documentation/web-api

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']

    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    result_dict = {}
    i = 0
    for result in json_result:
        result_dict[i] = result
        i += 1

    return result_dict

def pull_artist_by_id(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result


def pull_artist_albums_by_id(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    return json_result


def pull_album_tracks_by_id(token, album_id):
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    return json_result



token = get_token()
print(token)


# murkage_dave_dict = search_for_artist(token, 'murkage dave')
# with open('murkage_dave_query.json', 'w', encoding='utf-8') as f:
#     json.dump(murkage_dave_dict, f, ensure_ascii=False, indent=4)

thursday_dict = search_for_artist(token, 'thursday')
with open('thursday_query.json', 'w', encoding='utf-8') as f:
    json.dump(thursday_dict, f, ensure_ascii=False, indent=4)


thursday_album_dict = pull_artist_albums_by_id(token, '61awhbNK16ku1uQyXRsQj5')
with open('thursday_albums.json', 'w', encoding='utf-8') as f:
    json.dump(thursday_album_dict, f, ensure_ascii=False, indent=4)


full_collapse_live_dict = pull_album_tracks_by_id(token, '6mrm3oPwDEXoxdX6WPNrs2')
with open('full_collapse_live.json', 'w', encoding='utf-8') as f:
    json.dump(full_collapse_live_dict, f, ensure_ascii=False, indent=4)
