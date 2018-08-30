import boto3
from ast import literal_eval
from database.dynamoDB.globals import globals
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id = globals.AWS_ACCESS_KEY,
    aws_secret_access_key = globals.AWS_SECRET_ACCESS_KEY,
    region_name = globals.AWS_REGION
    )


def getRoutesTable():

    table = dynamodb.Table('Routes')
    return table.scan()


def getUsersTable():

    table = dynamodb.Table('DINO_Users')
    return table.scan()

def getRoutes():
    """
    Liefert alle Routen aus der DB in verschönerter Form
    :return: Alle Routen aus der DB in verschönerter Form
    """
    table = dynamodb.Table('Routes')
    routes_raw = table.scan()

    routes = reformat(routes_raw, "routes")

    return routes

def getRouteByID(id):
    table = dynamodb.Table('Routes')
    route_raw = table.query(KeyConditionExpression=Key('routeID').eq(id))

    #route = reformat(route_raw, "routes")

    return route_raw

def getRoutesByName(name):
    table = dynamodb.Table('Routes')
    route_raw = table.scan(KeyConditionExpression=Key('name').contains(name))

    routes = reformat(route_raw, "routes")

    return routes

def getUserByID(id):
    table = dynamodb.Table('DINO_Users')
    user_raw = table.query(KeyConditionExpression=Key('userID').eq(id))

    user = reformat(user_raw, "users")

    return user

def getUsers():
    """
    Liefert alle User aus der DB in verschönerter Form
    :return: Alle User aus der DB in verschönerter Form
    """

    table = dynamodb.Table('DINO_Users')
    users_raw = table.scan()

    users = reformat(users_raw, "users")

    return users

def reformat(data, table):
    """
    Entfernt die AWS Daten am Ende und führt die Daten in die Form {ID:{content},...} über.
    :param data: Die zu verarbeiteten Rohdaten von AWS
    :param table: Parameter, um welche Daten es sich handelt
    :return: Dictionary in der gewünschen Form
    """

    if table == "routes":
        return {element['routeID']: element['route'] for element in data['Items']}
        #return { (element['routeID']):(literal_eval(element['route']) if isinstance(element['route'], str)
          #else element['route']) for element in data['Items'] }
    elif table == "users":
        return {element['userID']: element for element in data['Items']}
    else:
        return None