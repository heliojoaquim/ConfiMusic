import boto3
import redis
from views.config import dynamodb_region
# Configuração do Redis
redis_client = redis.Redis(host='localhost',port=6379, db=0)

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=dynamodb_region)
table = dynamodb.Table('transactions')

def get(artist_name):
    return table.get_item(Key={'artist_name': artist_name})

