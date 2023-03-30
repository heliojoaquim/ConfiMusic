import boto3
from botocore.exceptions import ClientError

# Set the variables
table_name = 'artistas'
key_schema = [
    {'AttributeName': 'artist', 'KeyType': 'HASH'},
    {'AttributeName': 'songTitle', 'KeyType': 'RANGE'}
]
attribute_definitions = [
    {'AttributeName': 'artist', 'AttributeType': 'S'},
    {'AttributeName': 'songTitle', 'AttributeType': 'S'}
]
provisioned_throughput = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
}

# Create the DynamoDB connection
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

# Create the table
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )
    print("Table created successfully:", table.table_name)

    # Wait for the table to exist before exiting
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print("Table already exists")
    else:
        print("Error creating table:", e)
