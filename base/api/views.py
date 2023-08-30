from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from ..models import Notes
from .serializers import NotesSerializer
# Create your views here.


@api_view(['GET'])
def getRoutes(request):

    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    print(user)
    notes = user.notes_set.all()
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)
