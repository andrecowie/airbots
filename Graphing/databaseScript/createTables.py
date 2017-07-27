import boto3

session = boto3.session.Session(profile_name="autrdproject")
client = session.client('dynamodb')

client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        }
    ],
    TableName='locations',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'name',
            'KeyType' : 'RANGE'
        }
    ]
)

client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        }
    ],
    TableName='events',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'title',
            'KeyType' : 'RANGE'
        }
    ]
)
