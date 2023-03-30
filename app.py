from flask import Blueprint, jsonify, Flask
import uuid
import requests
import redis
import boto3
from dotenv import load_dotenv
import os
load_dotenv()

client_access_token = os.getenv('GENIUS_API_TOKEN')
if not client_access_token:
    raise ValueError('GENIUS_ACCESS_TOKEN não definido')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
dynamodb_region = os.getenv('DYNAMODB_REGION')
dynamodb_table_name = os.getenv('DYNAMODB_TABLE_NAME')



app = Flask(__name__)

# Conexão com o Redis
redis_client = redis.Redis(redis_host, redis_port)

# Conexão com o DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=dynamodb_region)

table = dynamodb.Table(dynamodb_table_name)

# Chaves de acesso ao Genius API
headers = {'Authorization': 'Bearer ' + client_access_token}

# Rota para buscar as 10 músicas mais populares de um artista
@app.route('/api/popular_songs/<artist_name>')
def popular_songs(artist_name):
    # Busca o artista no Genius API
    search_url = f'https://api.genius.com/search?q={artist_name}'
    search_response = requests.get(search_url, headers=headers).json()

    # Pega o ID do artista mais relevante na busca
    artist_id = search_response['response']['hits'][0]['result']['primary_artist']['id']

    # Busca as 10 músicas mais populares do artista
    songs_url = f'https://api.genius.com/artists/{artist_id}/songs?sort=popularity&per_page=10'
    songs_response = requests.get(songs_url, headers=headers).json()

    # Salva o ID de transação no DynamoDB
    transaction_id = str(uuid.uuid4())
    table.put_item(Item={
        'transaction_id': transaction_id,
        'artist_name': artist_name
    })


    return jsonify(songs_response)