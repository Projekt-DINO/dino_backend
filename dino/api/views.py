import boto3
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer
#from dino.database.dynamoDB.get_table_content import getRoutesTable
from database.dynamoDB.get_table_content import getRoutes, getUsers, getRouteByID
#from database.dynamoDB.globals import globals



# List all Stocks or create a new one
# /stocks/
class StockList(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class RoutesList(APIView):
    def get(self, request):

        route_infos = getRoutes()

        return Response(route_infos)

class RoutesListID(APIView):
    # funktioniert noch nicht. Er geht durch die URL noch nicht in diesen Fall.
    def get(self, **kwargs):
        route_infos = getRouteByID(id = kwargs['route_id'])

        return Response(route_infos)

class UserList(APIView):
    def get(self, request):
        users = getUsers()

        return Response(users)
