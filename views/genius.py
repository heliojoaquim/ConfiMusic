import requests
from views.config import client_access_token

headers = {'Authorization': 'Bearer ' + client_access_token}

def retrieve_songs_from_genius_api(artist_name):
    # Busca o artista no Genius API
    search_url = f'https://api.genius.com/search?q={artist_name}'
    search_response = requests.get(search_url, headers=headers).json()

    # Pega o ID do artista mais relevante na busca
    artist_id = search_response['response']['hits'][0]['result']['primary_artist']['id']

    # Busca as 10 músicas mais populares do artista
    songs_url = f'https://api.genius.com/artists/{artist_id}/songs?sort=popularity&per_page=10'
    songs_response = requests.get(songs_url, headers=headers).json()

    return songs_response
