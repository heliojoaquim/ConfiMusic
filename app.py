from flask import Blueprint, jsonify, Flask, request
import uuid
import requests
import redis
import boto3
from dotenv import load_dotenv
import os
import json

load_dotenv()
sete_dias = 604800
client_access_token = os.getenv('GENIUS_API_TOKEN')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
dynamodb_region = os.getenv('DYNAMODB_REGION')
dynamodb_table_name = os.getenv('DYNAMODB_TABLE_NAME')

app = Flask(__name__)

# Conexão com o Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)
if not redis_client:
    print("Não houve conexão com o servidor redis.")
# Conexão com o DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=dynamodb_region)
table = dynamodb.Table(dynamodb_table_name)
if not dynamodb:
    print("Não houve conexão com o servidor redis.")
# Chaves de acesso ao Genius API
headers = {'Authorization': 'Bearer ' + client_access_token}

# Rota para buscar as 10 músicas mais populares de um artista
@app.route('/popular_songs/<artist_name>')
def popular_songs(artist_name):
    cache_check(artist_name)
    # Verifica se a transação já está salva no DynamoDB
    response = table.get_item(Key={'artist_name': artist_name})
    if 'Item' in response:
        transaction_id = response['Item']['transaction_id']
        cache_enabled = response['Item'].get('cache_enabled', True)
        # Verifica se os dados já estão em cache no Redis
        cached_data = redis_client.get(artist_name)
        if cached_data and cache_enabled:
            songs_response = json.loads(cached_data)
        else:
            songs_response = retrieve_songs_from_genius_api(artist_name)
            redis_client.setex(artist_name, sete_dias, json.dumps(songs_response))
    else:
        songs_response = retrieve_songs_from_genius_api(artist_name)
        transaction_id = str(uuid.uuid4())
        table.put_item(Item={'transaction_id': transaction_id, 'artist_name': artist_name, 'cache_enabled': True})
        redis_client.setex(artist_name, sete_dias, json.dumps(songs_response))

    return jsonify(songs_response)

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

def cache_check(artist_name):
    cache = request.args.get('cache', default='True')
    if cache.lower() == 'false':
        # Remove dados do cache Redis
        redis_client.delete(artist_name)
        # Atualiza opção no DynamoDB
        table.update_item(
            Key={'artist_name': artist_name},
            UpdateExpression='SET cache_enabled = :val',
            ExpressionAttributeValues={':val': False}
        )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
