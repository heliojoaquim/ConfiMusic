from flask import request
import json
from views.database import redis_client, table, time_out

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