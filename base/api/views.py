from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .tokens import create_jwt_pair_for_user
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
# Create your views here.


@api_view(['GET'])
def getRoutes(request):

    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)



class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        #print(username)
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user) 
           
            
            return Response(
                {"message": "Login Successful", "tokens": tokens},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED)
