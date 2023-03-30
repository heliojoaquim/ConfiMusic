import os
from dotenv import load_dotenv

load_dotenv()


client_access_token = os.getenv('GENIUS_API_TOKEN')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
time_out = os.getenv('REDIS_TIMEOUT')
redis_password = os.getenv('REDIS_PASSWORD')
dynamodb_region = os.getenv('DYNAMODB_REGION')
dynamodb_table_name = os.getenv('DYNAMODB_TABLE_NAME')
