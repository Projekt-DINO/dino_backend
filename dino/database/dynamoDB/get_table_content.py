import boto3
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = 'AKIAJOS5HL35USFAR4YA',
    aws_secret_access_key = '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',
    region_name = 'eu-west-1'
    )

table = dynamodb.Table('Routes')

data = table.scan()

print(data)