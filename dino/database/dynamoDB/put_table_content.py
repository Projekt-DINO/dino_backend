import boto3
from generateID import ID
import globals

random_id = ID.generate_id()

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = globals.AWS_ACCESS_KEY,
    aws_secret_access_key = globals.AWS_SECRET_ACCESS_KEY,
    region_name = globals.AWS_REGION
    )

table = dynamodb.Table('Routes')

response = table.put_item(Item={
    "routeID": str(random_id)
    }
)

if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("success")
else:
    print("Failed")
