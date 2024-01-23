from forum.models import Post,CustomUser
from forum.serializers import PostSerializer,UserSerializer,MyTokenObtainPairSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simple_api_key.permissions import IsActiveEntity

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework_simple_api_key.permissions import IsActiveEntity
 
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PostList(generics.ListAPIView):
    queryset  = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostCreate(generics.CreateAPIView):
    uthentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset  = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        
   
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsActiveEntity]


class UserListCreate(generics.ListCreateAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = UserSerializer

    
    def create_api_key(self, request, *args, **kwargs):
        customUser = self.get_object()
        _, key = UserAPIKey.objects.create_api_key(name=" Api Key", entity=customUser)
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the user first
        self.perform_create(serializer)

        # Retrieve the created user's ID
        user_id = serializer.instance.id

        # Use the retrieved user ID to create the API key
        try:
            custom_user = CustomUser.objects.get(pk=user_id)
            result = self.create_api_key(custom_user)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED, headers=headers)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

