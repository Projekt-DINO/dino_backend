import boto3
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer
#from dino.database.dynamoDB.get_table_content import getRoutesTable
from database.dynamoDB.get_table_content import getRoutes, getUsers, getRouteByID, getUserByID, getRoutesByName
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
    def get(self, request, route_id):

        route_infos = getRouteByID(id = self.kwargs['route_id'])

        return Response(route_infos)

class RoutesListName(APIView):
    def get(self, request, route_name):

        route_infos = getRoutesByName(name = self.kwargs['route_name'])

        return Response(route_infos)

class UserList(APIView):
    def get(self, request):
        users = getUsers()

        return Response(users)

class UserListID(APIView):
    def get(self, request, user_id):

        user_infos = getUserByID(id = self.kwargs['user_id'])

        return Response(user_infos)