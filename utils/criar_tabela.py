import boto3
dynamodb = boto3.resource('dynamodb','sa-east-1')

table = dynamodb.create_table(
    TableName='ConfiMusic',
    KeySchema=[
        {
            'AttributeName': 'artist_name',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'artist_name',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
