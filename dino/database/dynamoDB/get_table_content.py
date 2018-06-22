import boto3
import globals

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = globals.AWS_ACCESS_KEY,
    aws_secret_access_key = globals.AWS_SECRET_ACCESS_KEY,
    region_name = globals.AWS_REGION
    )

table = dynamodb.Table('Routes')

data = table.scan()

print(data)