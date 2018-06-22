import boto3
from globals import globals

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = globals.AWS_ACCESS_KEY,
    aws_secret_access_key = globals.AWS_SECRET_ACCESS_KEY,
    region_name = globals.AWS_REGION
    )


def getRoutesTable():

    table = dynamodb.Table('Routes')
    return table.scan()

print(getRoutesTable())


def getUsersTable():

    table = dynamodb.Table('DINO_Users')
    return table.scan()

print(getUsersTable())