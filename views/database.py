import boto3
import redis
from views.config import dynamodb_region, dynamodb_table_name, redis_host, redis_password, redis_port

# Configuração do Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=dynamodb_region)
table = dynamodb.Table(dynamodb_table_name)

def get(artist_name):
    return table.get_item(Key={'artist_name': artist_name})
# Variável que armazena o tempo de 7 dias de expiração do Redis
time_out = 604800