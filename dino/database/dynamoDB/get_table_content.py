import boto3
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = '',
    aws_secret_access_key = '',
    region_name = 'eu-west-1'
    )

table = dynamodb.Table('Routes')

data = table.scan()

print(data)