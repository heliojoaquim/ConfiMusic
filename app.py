from flask import Flask, jsonify
import uuid
import json
from views.config import *
from views.database import *
from views.genius import *
from views.cache import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False



headers = {'Authorization': 'Bearer ' + client_access_token}

def get_songs_response(artist_name):
    cache_check(artist_name)
    response = table.get_item(Key={'artist_name': artist_name})

    if 'Item' in response:
        transaction_id = response['Item']['transaction_id']
        cache_enabled = response['Item'].get('cache_enabled', True)
        print(cache_enabled)
        cached_data = redis_client.get(artist_name)

        if cached_data and cache_enabled:
            songs_response = json.loads(cached_data)
        else:
            songs_response = retrieve_songs_from_genius_api(artist_name)
            redis_client.setex(artist_name, time_out, json.dumps(songs_response))
    else:
        songs_response = retrieve_songs_from_genius_api(artist_name)
        transaction_id = str(uuid.uuid4())
        table.put_item(Item={'transaction_id': transaction_id, 'artist_name': artist_name, 'cache_enabled': True})
        redis_client.setex(artist_name, time_out, json.dumps(songs_response))

    return songs_response

@app.route('/popular_songs/<artist_name>')
def popular_songs(artist_name):
    songs_response = get_songs_response(artist_name)
    return jsonify(songs_response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
