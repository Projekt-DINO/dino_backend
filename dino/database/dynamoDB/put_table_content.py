import boto3
from generateID import ID
from globals import globals

random_id = ID.generate_id()

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = globals.AWS_ACCESS_KEY,
    aws_secret_access_key = globals.AWS_SECRET_ACCESS_KEY,
    region_name = globals.AWS_REGION
    )

def putIntoRoutes():

    table = dynamodb.Table('Routes')

    response = table.put_item(Item={
        "bbox": "",
        "features": "",
        "info": "",
        "routeID": str(random_id),
        "type": "FeatureCollection"
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Added route into table - successful")
    else:
        print("Failed to insert route into table")


def putIntoDINOUsers():

    table = dynamodb.Table('DINO_Users')

    response = table.put_item(Item={
        "firstname": "Alexander",
        "lastname": "Teusz",
        "email": "alexander.teusz@hhu.de",
        "password": "ungehashtespasswort",
        "userID": str(random_id),
        "score": 400
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Added user into table - successful")
    else:
        print("Failed to insert user into table")

putIntoDINOUsers()
