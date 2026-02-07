from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all() 
    
    serializer_class = RegisterSerializer
    permission_classes=[AllowAny]
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Access Granted!",
            "user": request.user.username,
            "email": request.user.email
        })
    