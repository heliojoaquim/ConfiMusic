from flask import request

import json
from views.redis_config import redis_client
from views.dynamodb import table
from views.config import time_out

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
    else:
        table.update_item(
            Key={'artist_name': artist_name},
            UpdateExpression='SET cache_enabled = :val',
            ExpressionAttributeValues={':val': True}
        )

def get_cached_data(artist_name):
    # Verifica se os dados já estão em cache no Redis
    cached_data = redis_client.get(artist_name)
    if cached_data:
        return json.loads(cached_data)
    else:
        return None

def set_cached_data(artist_name, data):
    redis_client.setex(artist_name, time_out, json.dumps(data))
